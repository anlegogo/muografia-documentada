// Prints the concrete run-manager class created by G4RunManagerType::Default.
#include <cxxabi.h>
#include <cstdlib>
#include <iostream>
#include <typeinfo>
#include "G4RunManager.hh"
#include "G4RunManagerFactory.hh"
int main()
{
  const char* env = std::getenv("G4RUN_MANAGER_TYPE");
  auto* rm = G4RunManagerFactory::CreateRunManager(G4RunManagerType::Default);
  int status = 0;
  char* name = abi::__cxa_demangle(typeid(*rm).name(), nullptr, nullptr, &status);
  std::cout << "RUN-MANAGER class=" << (status == 0 ? name : typeid(*rm).name())
            << " factory_default=" << G4RunManagerFactory::GetDefault()
            << " G4RUN_MANAGER_TYPE=" << (env ? env : "(unset)") << std::endl;
  std::free(name);
  delete rm;
  return 0;
}
