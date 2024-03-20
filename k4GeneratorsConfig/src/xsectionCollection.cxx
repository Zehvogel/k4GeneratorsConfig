#include "xsectionCollection.h"
#include <filesystem>
#include <iostream>
#include <sys/stat.h>

k4GeneratorsConfig::xsectionCollection::xsectionCollection()
{

}
k4GeneratorsConfig::xsectionCollection::~xsectionCollection(){
}
void k4GeneratorsConfig::xsectionCollection::makeCollection(){

  for (const auto& yamls : std::filesystem::directory_iterator(".")) {
    std::filesystem::path yamlsPath = yamls.path();
    if ( yamlsPath.extension() == ".yaml" ) continue;
    for (const auto& generators : std::filesystem::directory_iterator(yamlsPath.string()+"/Run-Cards")) {
      std::filesystem::path generatorsPath = generators.path();
      for (const auto& procs : std::filesystem::directory_iterator(generatorsPath.string())) {
	std::filesystem::path processPath = procs.path();
	for (const auto& files : std::filesystem::directory_iterator(processPath.string())) {
	  std::filesystem::path filenamePath = files.path();
	  if ( filenamePath.extension() == ".edm4hep" ){
	    std::cout << "Adding " << filenamePath.string() << " to list" << std::endl;
	    k4GeneratorsConfig::xsection xsec;
	    xsec.setProcess(processPath.filename().string());
	    xsec.setGenerator(generatorsPath.filename().string());
	    xsec.setFile(filenamePath.string());
	    m_xsectionCollection.push_back(xsec);
	  }
	}
      }
    }
  }

}
void k4GeneratorsConfig::xsectionCollection::Print(){

  for (auto xsec: m_xsectionCollection){
    xsec.Print();
  }
}
