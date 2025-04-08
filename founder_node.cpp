#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class FounderNode : public rclcpp::Node
{
public:
    FounderNode() : Node("founder_node")
    {
        // 获取参数
        this->declare_parameter("ekf.xyz", std::vector<double>({0.50, 0.50, 0.50}));
        this->declare_parameter("ekf.yaw", 0.355);
        this->declare_parameter("ekf.r", 0.802);
        this->declare_parameter("vx", 2);
        this->declare_parameter("vy", 1);
        this->declare_parameter("vz", 3);

        // 从参数服务器中获取值
        auto ekf_xyz = this->get_parameter("ekf.xyz").as_double_array();
        auto ekf_yaw = this->get_parameter("ekf.yaw").as_double();
        auto ekf_r = this->get_parameter("ekf.r").as_double();
        auto vx = this->get_parameter("vx").as_int();
        auto vy = this->get_parameter("vy").as_int();
        auto vz = this->get_parameter("vz").as_int();

        // 输出确认
        RCLCPP_INFO(this->get_logger(), "ekf.xyz: [%f, %f, %f]", ekf_xyz[0], ekf_xyz[1], ekf_xyz[2]);
        RCLCPP_INFO(this->get_logger(), "ekf.yaw: %f", ekf_yaw);
        RCLCPP_INFO(this->get_logger(), "ekf.r: %f", ekf_r);
        RCLCPP_INFO(this->get_logger(), "vx: %d", vx);
        RCLCPP_INFO(this->get_logger(), "vy: %d", vy);
        RCLCPP_INFO(this->get_logger(), "vz: %d", vz);

        // 定时器，每秒发布一次
        timer_ = this->create_wall_timer(
            std::chrono::seconds(1),
            [this, ekf_xyz, ekf_yaw, ekf_r, vx, vy, vz]() {
                auto msg = std_msgs::msg::String();
                msg.data = "Sending parameters to tracker node";
                publisher_->publish(msg);
            });

        publisher_ = this->create_publisher<std_msgs::msg::String>("tracker_params", 10);
    }

private:
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<FounderNode>());
    rclcpp::shutdown();
    return 0;
}
