import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

def train(rank, world_size):
    dist.init_process_group("gloo", rank=rank, world_size=world_size)
    model = torch.nn.Linear(10, 10).to(rank)
    ddp_model = DDP(model, device_ids=[rank])
    optimizer = torch.optim.SGD(ddp_model.parameters(), lr=0.001)

    # Example of a train loop
    for _ in range(100):
        optimizer.zero_grad()
        output = ddp_model(torch.randn(20, 10).to(rank))
        loss = output.sum()
        loss.backward()
        optimizer.step()

    dist.destroy_process_group()

if __name__ == "__main__":
    world_size = 2 
    torch.multiprocessing.spawn(train, args=(world_size,), nprocs=world_size)