#!/usr/bin/env python3

import os
import json
from pathlib import Path
from datetime import datetime
import glob
import random

random.seed(42)

#SECONDS_PER_TRIAL = 11
#MINUTES_PER_STUDY = 15
# 15 minutes x 11 seconds per trial = 81 trials
TRIALS_PER_STUDY = 75

def generate_config(experiment_dir):
    """Generate config JSON for an experiment."""
    base_path = Path(experiment_dir)
    
    # Find all WAV files
    wav_files = glob.glob(str(base_path / "**/*.wav"), recursive=True)
    reference_files = [f for f in wav_files if '-reference.wav' in f]
    
    # Group into trials
    trials = []
    for ref in reference_files:
        trans = ref.replace('-reference.wav', '.wav')
        if trans in wav_files:
            trials.append({
                #"reference": str(Path(ref).relative_to(base_path.parent)),
                #"transformed": str(Path(trans).relative_to(base_path.parent)),
                "reference": ref,
                "transformed": trans,
                "metadata": json.loads(open(trans.replace('.wav', '.json')).read())
            })

    random.shuffle(trials)
    
    # Create studies
    num_studies = len(trials) // TRIALS_PER_STUDY
    studies = []
    for i in range(num_studies):
        start = i * TRIALS_PER_STUDY
        end = start + TRIALS_PER_STUDY
        studies.append({
            "name": f"study_{i+1:03d}",
            "trials": trials[start:end]
        })

    config = {
        "experiments": [{
            "name": base_path.name,
            "studies": studies
        }]
    }

    return config

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("experiment_dir", help="Directory containing experiment WAV files")
    args = parser.parse_args()

    config = generate_config(args.experiment_dir)

    os.makedirs('config', exist_ok=True)
    config_path = f'config/{Path(args.experiment_dir).name}.json'

    if os.path.exists(config_path):
        raise FileExistsError(f"Config file already exists: {config_path}")
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Generated {config_path}")
    print(f"Studies: {len(config['experiments'][0]['studies'])}")
    print(f"Total trials: {sum(len(s['trials']) for s in config['experiments'][0]['studies'])}")

if __name__ == '__main__':
    main()