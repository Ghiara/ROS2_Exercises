#include "rclcpp/rclcpp.hpp"

int main(int argc, char **argv){
    /* init the rclcpp */
    rclcpp::init(argc, argv);
    // generate a node_01 node
    auto node = std::make_shared<rclcpp::Node>("node_01");
    // print a self introduction
    RCLCPP_INFO(node->get_logger(), "node_01 activated.");
    // initiate node, detect the withdraw signal
    rclcpp::spin(node);
    // stop the initiation
    rclcpp::shutdown();
    return 0;
}