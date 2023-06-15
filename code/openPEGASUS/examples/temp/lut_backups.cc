#include "pegasus/pegasus_runtime.h"
#include "pegasus/timer.h"
#include <iostream>
#include <vector>
#include <cstdio>
#include <string>
#include <cstring>
#include <cmath>
#include <ctime>
#include <fstream>
#include <numeric>
#include <algorithm>
#include <stack>
#include <map>


using namespace std;
const int N = 16;//数据集大小
vector<vector<double>> ncopyx;
vector<vector<double>> ncopyy;
int clusterID = 0;


class point{
public:
	int cluster=0;
	int pointType=1;//1 noise 2 border 3 core
	int pts=0;//points in MinPts 
	int visited = 0;
	int corePointID = -1;
	vector<int> corepts;
	vector<int> allpts;//所有的points in MinPts
	vector<int> neighbors;
	point(){};
};

//读文件，分别将数据的x坐标与y坐标读入两个向量中
void openFile(const char* dataset, vector<double> &x0, vector<double> &y0){
	fstream infile;
	infile.open(dataset,ios::in);    //dataset在main函数中指定文件名
	if(!infile.is_open()) 
        cout <<"Open File Failed!" <<endl;
    string temp,ycut;
    int i;
    while(getline(infile,temp))
    {
       x0.push_back(stod(temp));
       vector<double> xx(N,stod(temp));
       int split = temp.find(';',0) + 1;
       ycut = temp.substr(split);
       y0.push_back(stod(ycut));
       vector<double> yy(N,stod(ycut));
       ncopyx.push_back(xx);
       ncopyy.push_back(yy);
    }
	infile.close();
	cout<<"Reading the dataset successful!!"<<endl;
    return;
}


int main() {
  using namespace gemini;
  PegasusRunTime::Parms pp;
  pp.lvl0_lattice_dim = lwe::params::n();
  pp.lvl1_lattice_dim = 1 << 12;
  pp.lvl2_lattice_dim = 1 << 16;
  pp.nlevels = 4;// CKKS levels
  pp.scale = std::pow(2., 40);
  pp.nslots = N;//  N
  pp.s2c_multiplier = 1.;

  PegasusRunTime pg_rt(pp,/*num_threads*/4);
  
  vector<double> xslots;
  vector<double> yslots;
  vector<double> dec;

  openFile("points.txt",xslots,yslots);
  for(int i=0;i<pp.nslots;i++){
    xslots[i]=xslots[i]/10;
    yslots[i]=yslots[i]/10;
  }
  
  vector<double> e(pp.nslots);
  for(int i=0;i<pp.nslots;i++)
	e[i]=0.3000001;

  Ctx ckks_xct;    //x1-xpp.nslots
  Ctx ckks_yct;    //y1-ypp.nslots
  Ctx r;           //r

  CHECK_AND_ABORT(pg_rt.EncodeThenEncrypt(xslots,ckks_xct));
  CHECK_AND_ABORT(pg_rt.EncodeThenEncrypt(yslots,ckks_yct));
  CHECK_AND_ABORT(pg_rt.EncodeThenEncrypt(e,r));

//x1~xn y1~yn分别加密成一个长度为n的
  vector<Ctx> x_value(pp.nslots);
  vector<Ctx> y_value(pp.nslots);

  size_t level = GetNModuli(ckks_xct);
  cout<<"ct level:"<<level<<endl;

  for(int i=0;i<pp.nslots;i++){
  CHECK_AND_ABORT(pg_rt.EncodeThenEncrypt(xslots[i],x_value[i]));
  CHECK_AND_ABORT(pg_rt.EncodeThenEncrypt(yslots[i], y_value[i]));
}


//(x-xi),(y-yi)
 for(int i =0; i < pp.nslots; i++){
  CHECK_AND_ABORT(pg_rt.Sub(x_value[i], ckks_xct));
  CHECK_AND_ABORT(pg_rt.Sub(y_value[i], ckks_yct));
 }

  size_t level3 = GetNModuli(x_value[0]);
  cout<<"x-xi level:"<<level3<<endl;

//(x-xi)^2,(y-yi)^2 relinethenrescale
for(int i=0;i<pp.nslots;i++){
  CHECK_AND_ABORT(pg_rt.Square(x_value[i]));
  CHECK_AND_ABORT(pg_rt.Square(y_value[i]));
  CHECK_AND_ABORT(pg_rt.RelinThenRescale(x_value[i]));
  CHECK_AND_ABORT(pg_rt.RelinThenRescale(y_value[i]));
}

size_t level2 = GetNModuli(x_value[0]);
  cout<<"reline&rescale level:"<<level2<<endl;

//r^2
CHECK_AND_ABORT(pg_rt.Square(r));
CHECK_AND_ABORT(pg_rt.RelinThenRescale(r));
CHECK_AND_ABORT(pg_rt.DecryptThenDecode(r,dec));

//(x-xi)^2+(y-yi)^2
for(int i=0;i<pp.nslots;i++)
  CHECK_AND_ABORT(pg_rt.Add(x_value[i],y_value[i]));

//(x-xi)^2+(y-yi)^2-r^2
for(int i=0;i<pp.nslots;i++)
  CHECK_AND_ABORT(pg_rt.Sub(x_value[i],r));

//SlotsToCoeffs & RelinThenRescale
for(int i=0;i<pp.nslots;i++){
  CHECK_AND_ABORT(pg_rt.SlotsToCoeffs(x_value[i]));
  //CHECK_AND_ABORT(pg_rt.RelinThenRescale(x_value[i]));
}

//ExtraAllCoefficients
std::vector<vector<lwe::Ctx_st>> lwe_ct(pp.nslots);//(N*0)->(N*N)
for(int j=0;j<pp.nslots;j++)
  CHECK_AND_ABORT(pg_rt.ExtraAllCoefficients(x_value[j],lwe_ct[j]));

//IsNegative判断是否大于0
std::function<double(double)> target_func;
target_func = [](double e) { return e>0.5 ? 1. : 0. ; };

for(int i=0;i<pp.nslots;i++)
  pg_rt.IsNegative(lwe_ct[i].data(),lwe_ct[i].size());



std::vector<lwe::Ctx_st> lwe_n(pp.nslots);
std::vector<lwe::Ctx_st> lwe_c(pp.nslots);
lwe::Ctx_st a,b;

//获得每个点的pits(即lwe_n[i])
for(int i=0;i<pp.nslots;i++){
  pg_rt.AddLWECt(a,lwe_ct[i][0],lwe_ct[i][1]);
  for(int j=2;j<pp.nslots-1;j++){
    if(j%2==0)
      pg_rt.AddLWECt(b,a,lwe_ct[i][j]);
    else
      pg_rt.AddLWECt(a,b,lwe_ct[i][j]);
  }
  if(pp.nslots%2==0)
    pg_rt.AddLWECt(lwe_n[i],b,lwe_ct[i][pp.nslots-1]);
  else
    pg_rt.AddLWECt(lwe_n[i],a,lwe_ct[i][pp.nslots-1]);
}

for(int i=0;i<pp.nslots;i++)
  cout<<pg_rt.DecryptLWE(lwe_n[i])<<"  ";
 cout<<endl<<endl;

//获得每个点iscore(即lwe_c[i])
for(int i=0;i<pp.nslots;i++)
  lwe_c[i]=lwe_n[i];

pg_rt.Sign(lwe_c.data(),lwe_c.size());

for(int i=0;i<pp.nslots;i++)
  cout<<target_func(pg_rt.DecryptLWE(lwe_c[i]))<<"  ";
cout<<endl<<endl;





//lwe_n[i]置1
pg_rt.AbsSqrt(lwe_n.data(),lwe_n.size());

//聚簇过程
for(int i=0;i<pp.nslots;i++){
  for(int j=0;j<pp.nslots;j++)
    cout<<target_func(pg_rt.DecryptLWE(lwe_ct[i][j]))<<"  ";
  cout<<" "<<target_func(pg_rt.DecryptLWE(lwe_c[i]));
  cout<<"  "<<target_func(pg_rt.DecryptLWE(lwe_n[i]));
  cout<<endl;
}cout<<endl;


std::vector<lwe::Ctx_st> lwe_temp(pp.nslots);
std::vector<lwe::Ctx_st> lwe_0;

for(int j=0;j<pp.nslots-1;j++){
  for(int i=j+1;i<pp.nslots;i++){
    pg_rt.AddLWECt(a,lwe_ct[i][j],lwe_c[i]);
    lwe_0.push_back(a);
    pg_rt.AddLWECt(b,a,lwe_c[j]);
    for(int k=0;k<pp.nslots;k++)
      pg_rt.AddLWECt(lwe_temp[k],b,lwe_ct[j][k]);
    pg_rt.Tanh(lwe_temp.data(),lwe_temp.size());    //lut n*n*(n-1)/2
    for(int k=0;k<pp.nslots;k++){
      a=lwe_ct[i][k];
      pg_rt.AddLWECt(lwe_ct[i][k],a,lwe_temp[k]);
    }
    pg_rt.ReLU(lwe_ct[i].data(),lwe_ct[i].size());  //lut n*n*(n-1)/2
  }
  pg_rt.AbsLog(lwe_0.data(),lwe_0.size());          //lut n
  for(int k=0;k<lwe_0.size();k++){
    pg_rt.SubLWECt(a,lwe_n[j],lwe_0[k]);
    lwe_n[j]=a;
  }
  lwe_0.clear();
}

pg_rt.ReLU(lwe_n.data(),lwe_n.size());              //lut 1

for(int i=0;i<pp.nslots;i++){
  for(int j=0;j<pp.nslots;j++)
    cout<<target_func(pg_rt.DecryptLWE(lwe_ct[i][j]))<<"  ";
  cout<<" "<<target_func(pg_rt.DecryptLWE(lwe_c[i]));
  cout<<"  "<<target_func(pg_rt.DecryptLWE(lwe_n[i]));
  cout<<endl;
}cout<<endl;



return 0;
}





















