from otter.test_files import test_case

OK_FORMAT = False

name = "q271"
points = None

@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_top_k_range(env):
    import torch
    fn = env['top_k_sample']
    logits = torch.randn(30)
    k = 5
    # Collect 200 samples and check all come from the top-k indices
    topk_idx = set(torch.topk(logits, k).indices.tolist())
    for _ in range(200):
        result = fn(logits.clone(), k=k)
        assert result in topk_idx, f'top_k_sample returned {result} which is not in top-{k}'

@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_top_k_deterministic_at_k1(env):
    import torch
    fn = env['top_k_sample']
    logits = torch.randn(30)
    best   = logits.argmax().item()
    # With k=1 and very low temperature, should always return the best token
    for _ in range(20):
        assert fn(logits.clone(), k=1, temperature=1e-6) == best

