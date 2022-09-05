#include "rclcpp/rclcpp.hpp"


int main(int argc, char **argv){
    // visit rclcpp init func
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<rclcpp::Node>("first_node"));
    return 0;
}