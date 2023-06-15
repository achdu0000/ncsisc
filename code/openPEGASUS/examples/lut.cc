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
#include <unordered_map>


using namespace std;
int N = 32;//数据集大小
vector<vector<double>> ncopyx;
vector<vector<double>> ncopyy;



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
  pp.nslots = N;
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
  vector<double> e_(pp.nslots);
  for(int i=0;i<pp.nslots;i++){
    e[i]=0.300001;
    e_[i]=1/0.300001;
  }
  Ctx ckks_xct;
  Ctx ckks_yct; 
  Ctx ckks_x_ans; 
  Ctx ckks_y_ans;
  Ctx r;
  Ctx r_;

  double time1{0.};
  AutoTimer timer1(&time1);
  CHECK_AND_ABORT(pg_rt.EncodeThenEncrypt(xslots,ckks_xct));
  CHECK_AND_ABORT(pg_rt.EncodeThenEncrypt(yslots,ckks_yct));
  timer1.stop();
  cout<<"加密时间为："<<time1<<" ms"<<endl;
  CHECK_AND_ABORT(pg_rt.EncodeThenEncrypt(xslots,ckks_x_ans));
  CHECK_AND_ABORT(pg_rt.EncodeThenEncrypt(yslots,ckks_y_ans));
  CHECK_AND_ABORT(pg_rt.EncodeThenEncrypt(e,r));
  CHECK_AND_ABORT(pg_rt.EncodeThenEncrypt(e_,r_));



//获取点在网格中的位置
  CHECK_AND_ABORT(pg_rt.Mul(ckks_x_ans,r_));
  CHECK_AND_ABORT(pg_rt.Mul(ckks_y_ans,r_));

//x1~xn y1~yn分别加密成一个长度为n的

  vector<Ctx> x_value(pp.nslots);
  vector<Ctx> y_value(pp.nslots);
  for(int i=0;i<pp.nslots;i++){
  CHECK_AND_ABORT(pg_rt.EncodeThenEncrypt(xslots[i],x_value[i]));
  CHECK_AND_ABORT(pg_rt.EncodeThenEncrypt(yslots[i], y_value[i]));
}



  double time2{0.};
  AutoTimer timer2(&time2);
//(x-xi),(y-yi)
 for(int i =0; i < pp.nslots; i++){
  CHECK_AND_ABORT(pg_rt.Sub(x_value[i], ckks_xct));
  CHECK_AND_ABORT(pg_rt.Sub(y_value[i], ckks_yct));
 }

//(x-xi)^2,(y-yi)^2 relinethenrescale
for(int i=0;i<pp.nslots;i++){
  CHECK_AND_ABORT(pg_rt.Square(x_value[i]));
  CHECK_AND_ABORT(pg_rt.Square(y_value[i]));
  CHECK_AND_ABORT(pg_rt.RelinThenRescale(x_value[i]));
  CHECK_AND_ABORT(pg_rt.RelinThenRescale(y_value[i]));
}

//r^2
CHECK_AND_ABORT(pg_rt.Square(r));
CHECK_AND_ABORT(pg_rt.RelinThenRescale(r));

//(x-xi)^2+(y-yi)^2
for(int i=0;i<pp.nslots;i++)
  CHECK_AND_ABORT(pg_rt.Add(x_value[i],y_value[i]));

//(x-xi)^2+(y-yi)^2-r^2
for(int i=0;i<pp.nslots;i++)
  CHECK_AND_ABORT(pg_rt.Sub(x_value[i],r));
timer2.stop();
cout<<"距离运算时间为："<<time2<<" ms"<<endl;

//SlotsToCoeffs & RelinThenRescale
double time3{0.};
AutoTimer timer3(&time3);
for(int i=0;i<pp.nslots;i++){
  CHECK_AND_ABORT(pg_rt.SlotsToCoeffs(x_value[i]));
  CHECK_AND_ABORT(pg_rt.RelinThenRescale(x_value[i]));
}
timer3.stop();
cout<<"S2C时间为："<<time3<<" ms"<<endl;


//ExtraAllCoefficients
double time4{0.};
AutoTimer timer4(&time4);

std::vector<vector<lwe::Ctx_st>> lwe_ct(pp.nslots);//(N*0)->(N*N)
for(int j=0;j<pp.nslots;j++)
  CHECK_AND_ABORT(pg_rt.ExtraAllCoefficients(x_value[j],lwe_ct[j]));
timer4.stop();
cout<<"Extract时间为："<<time4<<" ms"<<endl;
  
//定义函数用于结果输出的取整
std::function<double(double)> target_func;
target_func = [](double e) { return e> 0.05 ? 1. : 0. ; };


//IsNegative判断是否大于0
double time5{0.};
AutoTimer timer5(&time5);

std::vector<lwe::Ctx_st> temp;
for(int i=0;i<pp.nslots;i++){
  for(int j=0;j<=i;j++)
    temp.push_back(lwe_ct[i][j]); 
  pg_rt.IsNegative(temp.data(),temp.size());
  for(int j=0;j<=i;j++){
    lwe_ct[i][j]=temp[j];
    lwe_ct[j][i]=temp[j];
  }
  temp.clear();
}
timer5.stop();
cout<<"LUT时间为："<<time5<<" ms"<<endl;

/*
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

//获得每个点iscore(即lwe_c[i])
for(int i=0;i<pp.nslots;i++)
  lwe_c[i]=lwe_n[i];

pg_rt.Sign(lwe_c.data(),lwe_c.size());


for(int i=0;i<pp.nslots;i++){
  for(int j=0;j<pp.nslots;j++)
    cout<<target_func(pg_rt.DecryptLWE(lwe_ct[i][j]))<<"  ";
  cout<<" "<<target_func(pg_rt.DecryptLWE(lwe_c[i]));
  cout<<endl;
}cout<<endl;
*/

std::ofstream outFile;
outFile.open("out.txt");

for(int i=0;i<pp.nslots;i++){
  for(int j=0;j<pp.nslots;j++)
    outFile<<target_func(pg_rt.DecryptLWE(lwe_ct[i][j]))<<";";
  outFile<<endl;
}



/*
for(int i=0;i<pp.nslots;i++){
  for(int j=0;j<pp.nslots;j++){
    if(j!=i){
      pg_rt.AddLWECt(a,lwe_ct[j][i],lwe_c[j]);
      pg_rt.SubLWECt(b,a,temp[0]);
      pg_rt.SubLWECt(a,b,temp[0]);
      temp[0]=a;
      pg_rt.Tanh(temp.data(),temp.size());
      cout<<target_func(pg_rt.DecryptLWE(temp[0]))<<";";
      pg_rt.AddLWECt(a,temp[0],lwe_b[i]);
      lwe_b[i]=a;
    }
    else{
      cout<<target_func(pg_rt.DecryptLWE(temp[0]))<<";";
      pg_rt.AddLWECt(a,temp[0],lwe_b[i]);
      lwe_b[i]=a;
    }
  }cout<<endl;
  pg_rt.AbsSqrt(temp.data(),temp.size());
}
*/

/*
std::vector<lwe::Ctx_st> lwe_b(pp.nslots);
std::vector<lwe::Ctx_st> temp(pp.nslots);

for(int i=0;i<pp.nslots;i++){
  lwe_b[i]=lwe_c[i];
  temp[i]=lwe_b[i];
}

pg_rt.Tanh(lwe_b.data(),lwe_b.size());
pg_rt.AbsSqrt(temp.data(),temp.size());

for(int i=0;i<pp.nslots;i++)
  cout<<pg_rt.DecryptLWE(lwe_b[i])<<" ";
cout<<endl;

for(int i=0;i<pp.nslots;i++){
  for(int j=0;j<pp.nslots;j++){
    pg_rt.AddLWECt(a,lwe_ct[i][j],lwe_c[i]);
    pg_rt.SubLWECt(b,a,temp[j]);
    pg_rt.SubLWECt(a,b,temp[j]);
    temp[j]=a;
  }
  pg_rt.Tanh(temp.data(),temp.size());
  for(int j=0;j<pp.nslots;j++){
    pg_rt.AddLWECt(a,temp[j],lwe_b[j]);
    lwe_b[j]=a;
  }
}


for(int i=0;i<pp.nslots;i++){
  for(int j=0;j<pp.nslots;j++)
    cout<<target_func(pg_rt.DecryptLWE(lwe_ct[i][j]))<<"  ";
  cout<<" "<<target_func(pg_rt.DecryptLWE(lwe_c[i]));
  cout<<" "<<pg_rt.DecryptLWE(lwe_b[i]);
  cout<<endl;
}cout<<endl;
*/





return 0;
}


















