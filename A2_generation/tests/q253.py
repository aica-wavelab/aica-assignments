from otter.test_files import test_case

OK_FORMAT = False

name = "q253"
points = None

@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_var_token_emb_params(env):
    assert 'token_emb_params' in env, 'variable token_emb_params is not initialized'
    expected = env['vocab_size_'] * env['n_embd_']
    assert env['token_emb_params'] == expected, 'wrong value for token_emb_params'

@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_var_pos_emb_params(env):
    assert 'pos_emb_params' in env, 'variable pos_emb_params is not initialized'
    expected = env['sequence_len_'] * env['n_embd_']
    assert env['pos_emb_params'] == expected, 'wrong value for pos_emb_params'

@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_var_params_per_head(env):
    assert 'params_per_head' in env, 'variable params_per_head is not initialized'
    expected = 3 * (env['n_embd_'] * env['head_size_'])
    assert env['params_per_head'] == expected, 'wrong value for params_per_head'

@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_var_W0_params(env):
    assert 'W0_params' in env, 'variable W0_params is not initialized'
    expected = (env['head_size_'] * env['n_heads_']) * env['n_embd_'] + env['n_embd_']
    assert env['W0_params'] == expected, 'wrong value for W0_params'

@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_var_ffn_params(env):
    assert 'ffn_params' in env, 'variable ffn_params is not initialized'
    n = env['n_embd_']
    expected = (n * (4 * n) + 4 * n) + ((4 * n) * n + n)
    assert env['ffn_params'] == expected, 'wrong value for ffn_params'

@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_var_layernorm_params(env):
    assert 'layernorm_params' in env, 'variable layernorm_params is not initialized'
    expected = 2 * (2 * env['n_embd_'])
    assert env['layernorm_params'] == expected, 'wrong value for layernorm_params'

@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_var_ln_f_params(env):
    assert 'ln_f_params' in env, 'variable ln_f_params is not initialized'
    expected = 2 * env['n_embd_']
    assert env['ln_f_params'] == expected, 'wrong value for ln_f_params'

@test_case(points=None, hidden=False, 
    success_message="correct!")
def test_var_lm_head_params(env):
    assert 'lm_head_params' in env, 'variable lm_head_params is not initialized'
    expected = env['n_embd_'] * env['vocab_size_'] + env['vocab_size_']
    assert env['lm_head_params'] == expected, 'wrong value for lm_head_params'

