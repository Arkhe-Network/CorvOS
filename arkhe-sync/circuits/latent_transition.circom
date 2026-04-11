pragma circom 2.1.0;

template LatentRollout(latent_dim) {
    signal input s_curr[latent_dim];
    signal input action[latent_dim];
    signal output s_next[latent_dim];

    for (var i = 0; i < latent_dim; i++) {
        s_next[i] <== s_curr[i] + action[i];
    }
}

component main = LatentRollout(256);
