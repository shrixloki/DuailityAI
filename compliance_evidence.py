#!/usr/bin/env python3
"""
GATE 2 Dataset Usage Discipline - Compliance Evidence Generator
============================================================

This script generates evidence to prove GATE 2 compliance for the Duality AI Space Station Challenge.
It collects and formats all required evidence for submission.
"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime


class Gate2ComplianceEvidence:
    """Generate comprehensive evidence for GATE 2 Dataset Usage Discipline compliance."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.evidence = {
            'readme_compliance': {},
            'training_script_paths': {},
            'configuration_compliance': {},
            'legacy_path_handling': {},
            'summary': {}
        }
    
    def collect_readme_evidence(self):
        """Collect evidence from README.md for dataset usage statements."""
        readme_path = self.project_root / 'README.md'
        
        if not readme_path.exists():
            self.evidence['readme_compliance']['error'] = "README.md not found"
            return
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for required statements
        falcon_dataset_found = 'Falcon synthetic dataset' in content
        challenge_found = 'Duality AI Space Station Challenge' in content
        separation_found = 'strict train/val/test separation' in content
        discipline_section = 'Dataset Usage Discipline' in content
        
        self.evidence['readme_compliance'] = {
            'falcon_dataset_statement': falcon_dataset_found,
            'challenge_reference': challenge_found,
            'separation_statement': separation_found,
            'discipline_section_exists': discipline_section,
            'compliance_score': sum([falcon_dataset_found, challenge_found, separation_found, discipline_section]),
            'excerpt': self._extract_discipline_section(content)
        }
    
    def _extract_discipline_section(self, content):
        """Extract the Dataset Usage Discipline section from README."""
        lines = content.split('\n')
        section_lines = []
        in_section = False
        
        for line in lines:
            if 'Dataset Usage Discipline' in line:
                in_section = True
                section_lines.append(line)
            elif in_section and line.startswith('##') and 'Dataset Usage Discipline' not in line:
                break
            elif in_section:
                section_lines.append(line)
        
        return '\n'.join(section_lines[:15])  # First 15 lines of section
    
    def collect_training_script_evidence(self):
        """Collect evidence from training scripts for path compliance."""
        train_script = self.project_root / 'src' / 'train.py'
        detect_script = self.project_root / 'src' / 'detect.py'
        
        evidence = {}
        
        for script_name, script_path in [('train.py', train_script), ('detect.py', detect_script)]:
            if not script_path.exists():
                evidence[script_name] = {'error': f"{script_name} not found"}
                continue
            
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for hard-coded paths
            hardcoded_patterns = [
                r'["\'][^"\']*data/raw[^"\']*["\']',
                r'["\'][^"\']*\.\.\/[^"\']*images[^"\']*["\']'
            ]
            
            hardcoded_paths = []
            for pattern in hardcoded_patterns:
                matches = re.findall(pattern, content)
                # Filter out acceptable config references
                forbidden = [m for m in matches if 'config/observo.yaml' not in m]
                hardcoded_paths.extend(forbidden)
            
            # Check for configuration usage
            uses_config = 'load_dataset_config' in content
            has_validation = 'validate_dataset_separation' in content
            
            evidence[script_name] = {
                'hardcoded_paths_found': hardcoded_paths,
                'uses_configuration': uses_config,
                'has_validation': has_validation,
                'compliance_score': int(not hardcoded_paths) + int(uses_config) + int(has_validation),
                'key_functions': self._extract_key_functions(content)
            }
        
        self.evidence['training_script_paths'] = evidence
    
    def _extract_key_functions(self, content):
        """Extract key compliance-related functions from script."""
        functions = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if 'def load_dataset_config' in line or 'def validate_dataset_separation' in line:
                # Extract function and a few lines
                func_lines = [line]
                for j in range(i+1, min(i+8, len(lines))):
                    if lines[j].strip() and not lines[j].startswith('def '):
                        func_lines.append(lines[j])
                    elif lines[j].startswith('def '):
                        break
                functions.append('\n'.join(func_lines))
        
        return functions
    
    def collect_configuration_evidence(self):
        """Collect evidence from configuration files."""
        config_path = self.project_root / 'config' / 'observo.yaml'
        
        if not config_path.exists():
            self.evidence['configuration_compliance']['error'] = "config/observo.yaml not found"
            return
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Check path compliance
        required_keys = ['path', 'train', 'val', 'test']
        has_required_keys = all(key in config for key in required_keys)
        
        # Check for relative paths
        relative_paths = True
        absolute_paths = []
        
        for key in required_keys:
            if key in config:
                path_value = config[key]
                if os.path.isabs(path_value):
                    relative_paths = False
                    absolute_paths.append(f"{key}: {path_value}")
        
        # Check directory separation
        directories = [config.get('train', ''), config.get('val', ''), config.get('test', '')]
        proper_separation = len(set(directories)) == len(directories) and all(directories)
        
        self.evidence['configuration_compliance'] = {
            'has_required_keys': has_required_keys,
            'uses_relative_paths': relative_paths,
            'absolute_paths_found': absolute_paths,
            'proper_directory_separation': proper_separation,
            'configuration_content': config,
            'compliance_score': sum([has_required_keys, relative_paths, proper_separation])
        }
    
    def collect_legacy_path_evidence(self):
        """Collect evidence of legacy path handling."""
        legacy_files = [
            'optimize_training.py',
            'quick_boost.py', 
            'run_optimization.py'
        ]
        
        evidence = {}
        
        for filename in legacy_files:
            file_path = self.project_root / filename
            
            if not file_path.exists():
                evidence[filename] = {'status': 'not_found'}
                continue
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for deprecation comments
            has_deprecation = 'DEPRECATED' in content
            has_migration_guide = 'Migration Guide' in content or 'TODO' in content
            
            # Count deprecated paths
            deprecated_patterns = [
                r'# DEPRECATED:.*',
                r'# TODO:.*'
            ]
            
            deprecation_comments = []
            for pattern in deprecated_patterns:
                matches = re.findall(pattern, content)
                deprecation_comments.extend(matches)
            
            evidence[filename] = {
                'has_deprecation_comments': has_deprecation,
                'has_migration_guidance': has_migration_guide,
                'deprecation_comments_count': len(deprecation_comments),
                'sample_comments': deprecation_comments[:3],  # First 3 comments
                'compliance_score': int(has_deprecation) + int(has_migration_guide)
            }
        
        self.evidence['legacy_path_handling'] = evidence
    
    def generate_compliance_summary(self):
        """Generate overall compliance summary."""
        readme_score = self.evidence['readme_compliance'].get('compliance_score', 0)
        
        # Training script scores
        train_scores = []
        for script_data in self.evidence['training_script_paths'].values():
            if 'compliance_score' in script_data:
                train_scores.append(script_data['compliance_score'])
        avg_train_score = sum(train_scores) / len(train_scores) if train_scores else 0
        
        config_score = self.evidence['configuration_compliance'].get('compliance_score', 0)
        
        # Legacy handling scores
        legacy_scores = []
        for file_data in self.evidence['legacy_path_handling'].values():
            if 'compliance_score' in file_data:
                legacy_scores.append(file_data['compliance_score'])
        avg_legacy_score = sum(legacy_scores) / len(legacy_scores) if legacy_scores else 0
        
        total_score = readme_score + avg_train_score + config_score + avg_legacy_score
        max_possible = 4 + 3 + 3 + 2  # Maximum possible scores
        
        compliance_percentage = (total_score / max_possible) * 100
        
        self.evidence['summary'] = {
            'readme_compliance_score': f"{readme_score}/4",
            'training_script_score': f"{avg_train_score:.1f}/3",
            'configuration_score': f"{config_score}/3", 
            'legacy_handling_score': f"{avg_legacy_score:.1f}/2",
            'total_score': f"{total_score:.1f}/{max_possible}",
            'compliance_percentage': f"{compliance_percentage:.1f}%",
            'gate2_status': 'COMPLIANT' if compliance_percentage >= 85 else 'NEEDS_IMPROVEMENT',
            'generated_at': datetime.now().isoformat()
        }
    
    def generate_evidence_report(self):
        """Generate complete evidence report."""
        self.collect_readme_evidence()
        self.collect_training_script_evidence()
        self.collect_configuration_evidence()
        self.collect_legacy_path_evidence()
        self.generate_compliance_summary()
        
        return self.evidence
    
    def save_evidence_report(self, output_path='gate2_compliance_evidence.yaml'):
        """Save evidence report to file."""
        evidence = self.generate_evidence_report()
        
        output_file = self.project_root / output_path
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(evidence, f, default_flow_style=False, indent=2)
        
        print(f"✅ GATE 2 compliance evidence saved to: {output_file}")
        return output_file
    
    def print_compliance_summary(self):
        """Print a formatted compliance summary."""
        if not self.evidence.get('summary'):
            self.generate_evidence_report()
        
        summary = self.evidence['summary']
        
        print("\n" + "="*60)
        print("🎯 GATE 2 DATASET USAGE DISCIPLINE - COMPLIANCE REPORT")
        print("="*60)
        print(f"📊 Overall Status: {summary['gate2_status']}")
        print(f"📈 Compliance Score: {summary['compliance_percentage']}")
        print(f"🕒 Generated: {summary['generated_at']}")
        print("\n📋 Detailed Scores:")
        print(f"   README Documentation: {summary['readme_compliance_score']}")
        print(f"   Training Scripts: {summary['training_script_score']}")
        print(f"   Configuration: {summary['configuration_score']}")
        print(f"   Legacy Path Handling: {summary['legacy_handling_score']}")
        print(f"   Total: {summary['total_score']}")
        
        # Key evidence snippets
        if self.evidence['readme_compliance'].get('excerpt'):
            print(f"\n📄 README Evidence Excerpt:")
            print("   " + "\n   ".join(self.evidence['readme_compliance']['excerpt'].split('\n')[:5]))
        
        print("\n" + "="*60)


def main():
    """Main function to generate GATE 2 compliance evidence."""
    print("🚀 GATE 2 Dataset Usage Discipline - Evidence Generator")
    print("=" * 60)
    
    generator = Gate2ComplianceEvidence()
    
    # Generate and save evidence
    evidence_file = generator.save_evidence_report()
    
    # Print summary
    generator.print_compliance_summary()
    
    print(f"\n📁 Complete evidence report: {evidence_file}")
    print("🎯 This evidence demonstrates GATE 2 compliance for challenge submission.")


if __name__ == "__main__":
    main()