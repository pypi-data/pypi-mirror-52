class Sharo:
    def __init__(self,node):
        self.node = node
        self.blackboard = node.new_pub("/blackboard","json")
        self.whiteboard = node.new_pub("/whiteboard","json")

    def update_blackboard(self, social_primtive,input_name, intensity, robot = "pepper"):
        data = {"primitive":social_primtive, "input":{input_name:intensity}, "robot":robot}
        self.blackboard.publish(data)

    def update_whiteboard(self, sensory_primtive,value,robot = "pepper"):
        data = {"primitive":sensory_primtive, "input":value, "robot":robot}
        self.blackboard.publish(data)




