variable "ec2_hpc_count" {}
variable "efa_enabled" {}
variable "braket_qpu_target" {}

resource "aws_instance" "hpc_node" {
  count         = var.ec2_hpc_count
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "hpc6a.48xlarge"

  tags = {
    Name = "arkhe-hpc-node-${count.index}"
  }
}
