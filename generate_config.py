#!/usr/bin/env python3

import os
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def generate_config(base_path):
    """
    Generate config JSON from directory structure.
    """
    base_path = Path(base_path)
    files_by_set = defaultdict(lambda: defaultdict(list))
    
    for root, _, files in os.walk(base_path):
        root_path = Path(root)
        
        # Get trial set and condition from path
        parts = root_path.parts
        if len(parts) < 3:  # Need at least base/trial_set/condition
            continue
            
        trial_set = parts[-2]  # e.g., to_annotate-TEST-000
        condition = parts[-1]  # e.g., to_annotate-TEST-000-descript_dac_44khz
        
        # Group files by their base ID
        file_groups = defaultdict(dict)
        
        for file in files:
            file_path = root_path / file
            # Note: removed base_path from relative path construction
            rel_path = str(file_path.relative_to(base_path.parent))
            
            # Extract ID and type
            if file.endswith('-reference.wav'):
                id = file.replace('-reference.wav', '')
                file_groups[id]['reference'] = rel_path
            elif file.endswith('.wav') and '-reference' not in file:
                id = file.replace('.wav', '')
                file_groups[id]['transformed'] = rel_path
            elif file.endswith('.json'):
                id = file.replace('.json', '')
                with open(file_path) as f:
                    try:
                        file_groups[id]['metadata'] = json.load(f)
                    except json.JSONDecodeError:
                        print(f"Warning: Could not parse JSON file: {file_path}")
                        file_groups[id]['metadata'] = {}
        
        # Add complete groups to files_by_set
        for id, group in file_groups.items():
            if 'reference' in group and 'transformed' in group:
                files_by_set[trial_set][condition].append({
                    'base_name': id,
                    'reference': group['reference'],
                    'transformed': group['transformed'],
                    'metadata': group.get('metadata', {})
                })
            elif 'reference' in group or 'transformed' in group:
                print(f"Warning: Incomplete pair for ID {id} in {condition}")

    config = {
        "version": "1.0",
        "metadata": {
            "name": "PURE Audio Annotation",
            "description": "3-AFC audio comparison task",
            "last_updated": datetime.now().strftime("%Y-%m-%d")
        },
        "media": {
            "base_url": "https://media.githubusercontent.com/media/pure-eval/pure-audio-to-annotate/refs/heads/main",
            "file_format": "wav"
        },
        "trial_sets": []
    }
    
    # Add trial sets
    for trial_set, conditions in sorted(files_by_set.items()):
        trial_set_config = {
            "id": trial_set,
            "conditions": []
        }
        
        for condition, files in sorted(conditions.items()):
            trial_set_config["conditions"].append({
                "id": condition,
                "files": sorted(files, key=lambda x: x['base_name'])
            })
            
        config["trial_sets"].append(trial_set_config)

    return config

def main():
    # Generate config
    print("Scanning to_annotate directory...")
    config = generate_config('to_annotate')
    
    # Create output directory
    os.makedirs('config', exist_ok=True)
    
    # Write config
    config_path = 'config/audio_config.json'
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"Generated {config_path}")
    
    # Print stats
    total_files = sum(
        len(condition["files"]) 
        for trial_set in config["trial_sets"] 
        for condition in trial_set["conditions"]
    )
    
    total_conditions = sum(
        len(trial_set["conditions"])
        for trial_set in config["trial_sets"]
    )
    
    print(f"\nStats:")
    print(f"Trial sets: {len(config['trial_sets'])}")
    print(f"Total conditions: {total_conditions}")
    print(f"Total file pairs: {total_files}")

if __name__ == '__main__':
    main()
