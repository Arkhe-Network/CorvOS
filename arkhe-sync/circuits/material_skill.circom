pragma circom 2.0.0;

template MaterialSkill(n_components) {
    signal input composition[n_components];
    signal input w_linear[n_components];
    signal output property;

    signal linear_sum[n_components];

    var sum = 0;
    for (var i = 0; i < n_components; i++) {
        sum += composition[i] * w_linear[i];
    }

    property <== sum;
}

component main = MaterialSkill(5);
