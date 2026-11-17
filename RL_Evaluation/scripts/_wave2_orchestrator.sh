#!/bin/bash
set -e
cd "$(dirname "$0")"

# Step 1: wait for the already-running gamma_0.99 job to finish
until grep -q 'DONE run=' ../logs/gamma_0.99.log 2>/dev/null; do
  sleep 15
done
echo "[orchestrator] gamma_0.99 finished at $(date)"

# Step 2: gamma_0.95, run to completion before continuing
python -u goal5_hyperparameter_sensitivity.py --dashboard small --episodes 100 --seed 42 \
  --lr 1e-2 --gamma 0.95 --run-label gamma_0.95 \
  --log-output ../results/goal5_training_log_gamma0.95.csv \
  --summary-csv ../results/goal5b_gamma_sweep.csv \
  > ../logs/gamma_0.95.log 2>&1
echo "[orchestrator] gamma_0.95 finished at $(date)"

# Step 3: single entropy-bonus run at current defaults (coef 0.01 only, per
# revised scope), run to completion.
python -u goal5_hyperparameter_sensitivity.py --dashboard small --episodes 100 --seed 42 \
  --lr 1e-2 --gamma 1.0 --entropy-coef 0.01 --run-label entropy_c0.01_default \
  --log-output ../results/goal5_training_log_entropy_default_c0.01.csv \
  --summary-csv ../results/goal5d_entropy_bonus.csv \
  > ../logs/entropy_c0.01_default.log 2>&1
echo "[orchestrator] entropy_c0.01_default finished at $(date)"

echo "[orchestrator] ALL WAVE 2 RUNS COMPLETE"
