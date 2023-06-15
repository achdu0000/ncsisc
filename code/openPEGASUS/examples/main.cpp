#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
using namespace std;

int N=128;

struct Point {
    double x;
    double y;
};

std::vector<Point> parseFile(const std::string& filename) {
    std::vector<Point> points;

    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cout << "Failed to open file: " << filename << std::endl;
        return points;
    }

    std::string line;
    while (std::getline(file, line)) {
        std::stringstream ss(line);
        std::string value;
        Point point;

        // Parse x and y values separated by ';'
        if (std::getline(ss, value, ';')) {
            std::stringstream(value) >> point.x;
        }
        if (std::getline(ss, value, ';')) {
            std::stringstream(value) >> point.y;
        }

        points.push_back(point);
    }

    file.close();
    return points;
}

void writeFile(const std::vector<Point>& points, std::vector<int> clusterLabels, const std::string& filename) {
    std::ofstream file(filename);
    if (!file.is_open()) {
        std::cout << "Failed to create file: " << filename << std::endl;
        return;
    }

    for (int i=0;i<N;i++) {
        file << points[i].x << ";" << points[i].y << ";" << clusterLabels[i]-1 << std::endl;
    }

    file.close();
    std::cout << "Successfully wrote data to file: " << filename << std::endl;
}


// Constants for cluster labels
const int UNCLASSIFIED = -1;
const int NOISE = 0;

std::vector<int> getNeighbors(const std::vector<std::vector<int>>& distanceMatrix, int pointIndex, double epsilon) {
    std::vector<int> neighbors;
    const std::vector<int>& distances = distanceMatrix[pointIndex];
    for (int i = 0; i < distances.size(); ++i) {
        if (i != pointIndex && distances[i] >= epsilon) {
            neighbors.push_back(i);
        }
    }
    return neighbors;
}

void expandCluster(const std::vector<std::vector<int>>& distanceMatrix, int pointIndex, int clusterId,
                   std::vector<int>& clusterLabels, double epsilon, int minPts) {
    std::vector<int> neighbors = getNeighbors(distanceMatrix, pointIndex, epsilon);
    if (neighbors.size() < minPts) {
        clusterLabels[pointIndex] = NOISE;
        return;
    }
    clusterLabels[pointIndex] = clusterId;
    for (int i = 0; i < neighbors.size(); ++i) {
        int neighborIndex = neighbors[i];
        if (clusterLabels[neighborIndex] == UNCLASSIFIED) {
            clusterLabels[neighborIndex] = clusterId;
            expandCluster(distanceMatrix, neighborIndex, clusterId, clusterLabels, epsilon, minPts);
        }
    }
}

std::vector<int> dbscan(const std::vector<std::vector<int>>& distanceMatrix, double epsilon, int minPts) {
    std::vector<int> clusterLabels(distanceMatrix.size(), UNCLASSIFIED);
    int clusterId = 1;
    for (int i = 0; i < distanceMatrix.size(); ++i) {
        if (clusterLabels[i] == UNCLASSIFIED) {
            std::vector<int> neighbors = getNeighbors(distanceMatrix, i, epsilon);
            if (neighbors.size() < minPts) {
                clusterLabels[i] = NOISE;
            } else {
                clusterLabels[i] = clusterId;
                expandCluster(distanceMatrix, i, clusterId, clusterLabels, epsilon, minPts);
                clusterId++;
            }
        }
    }
    return clusterLabels;
}

std::vector<int> readDataFromFile(const std::string& filename) {
    std::vector<int> data;
    std::ifstream file(filename);
    
    if (!file.is_open()) {
        std::cout << "Failed to open file: " << filename << std::endl;
        return data;
    }
    
    int value;
    while (file >> value) {
        data.push_back(value);
    }
    
    file.close();
    return data;
}

int main() {
    std::ifstream file("out128.txt");
    std::string line;
    std::vector<std::vector<int>> matrix;

    // 逐行读取文件
    while (std::getline(file, line)) {
        std::vector<int> row;
        std::istringstream iss(line);
        std::string token;
        // 以分号为分隔符分割每行的数字
        while (std::getline(iss, token, ';')) {
            int num = std::stoi(token);
            row.push_back(num);
        }
        // 将当前行的数据存储到二维vector中
        matrix.push_back(row);
    }


	double epsilon = 0.5;
    int minPts = 4;

    std::vector<int> clusterLabels = dbscan(matrix, epsilon, minPts);

	vector<Point> points = parseFile("date128.txt");

	writeFile(points, clusterLabels ,"result128.txt");

	std::vector<int> dataArray = readDataFromFile("test128.txt");

	double sum=0;
	for(int i=0;i<N;i++){
	  //cout<<dataArray[i]<<" "<<clusterLabels[i]<<endl;
	  if(dataArray[i]==(clusterLabels[i]-1))sum++;
	  dataArray[i]++;
	}

	cout<<"准确率为: "<<sum/N*100<<" %"<<endl;;

	writeFile(points, dataArray ,"actual_result128.txt");

    return 0;
}
