from otter.test_files import test_case

OK_FORMAT = False

name = "q291"
points = None

@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_lora_zero_init(env):
    """With lora_B=0 the LoRA output must equal the frozen linear output."""
    LoRALinear_ = env['LoRALinear']
    lin  = env['nn'].Linear(8, 16, bias=False)
    lora = LoRALinear_(lin, rank=2, alpha=2)
    x    = env['torch'].randn(3, 8)
    with env['torch'].no_grad():
        out_lora = lora(x)
        out_lin  = lin(x)
    assert out_lora.shape == out_lin.shape, 'Output shape mismatch'
    assert env['torch'].allclose(out_lora, out_lin, atol=1e-5), \
        'With lora_B=0, LoRALinear output should equal the frozen linear output.'

@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_lora_delta_applied(env):
    """With non-zero lora_B, the LoRA delta should be added to the output."""
    LoRALinear_ = env['LoRALinear']
    lin  = env['nn'].Linear(8, 16, bias=False)
    lora = LoRALinear_(lin, rank=2, alpha=4)   # scale = alpha/rank = 2
    with env['torch'].no_grad():
        lora.lora_B.fill_(0.1)   # make B non-zero
    x = env['torch'].randn(3, 8)
    with env['torch'].no_grad():
        out_lora = lora(x)
        out_lin  = lin(x)
    assert out_lora.shape == (3, 16), f'Expected shape (3, 16), got {out_lora.shape}'
    assert not env['torch'].allclose(out_lora, out_lin, atol=1e-5), \
        'With non-zero lora_B, LoRALinear output should differ from the frozen linear.'

