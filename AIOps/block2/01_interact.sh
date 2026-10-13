
## Create Working directory
mkdir docker-cpp-demo
cd docker-cpp-demo

## Create a C++ file: hello.cpp
# include <iostream>
# int main() {
#    std::cout << "Hello from C++ inside Docker!" << std::endl;
#    return 0;
# }

# Step 1. Pull the image
docker pull gcc:14

# Step 2. Run a container
# -d runs in the background
# -i keeps standard input open, 
# -t allocates a terminal
# Running bash as the container's main process 
# allows it to stay alive while you work
docker run -dit --name cpp-manual-demo gcc:14 bash

# Verify
docker ps

# Step 3. Copy the C++ file into the running container
docker cp hello.cpp cpp-manual-demo:/hello.cpp

# Step 4. Enter the running container
docker exec -it cpp-manual-demo bash

# Your terminal is now inside the container. For example, the prompt might look like:
# root@a1b2c3d4e5f6:/#

# Step 5. Compile and run the program
# g++ /hello.cpp -o /hello
# /hello

# Hello from C++ inside Docker!

# Step 6. Exit the container's shell
exit

# Notice that you have exited the interactive shell, 
# but the container should still be running because its original bash process remains active.
docker ps

# Step 7. Stop the container
docker stop cpp-manual-demo

# Step 8. Restart the container
docker start cpp-manual-demo

# Step 9. Re-Enter the running container
docker exec -it cpp-manual-demo bash

# Step 10. Exit the container's shell
exit

# check status
docker ps

# Stop the container
docker stop cpp-manual-demo

# Verify 
docker ps 
docker ps -a

# Step 11. Remove the container
docker rm cpp-manual-demo

# Verify 
docker ps 
docker ps -a

# Step 12. Remove the image
docker image rm gcc:14

# Verify 
docker images
