"""
Unit tests for GATE 2 Dataset Usage Discipline compliance verification.
Tests README.md content for required dataset usage statements.
"""

import os
import pytest


class TestREADMECompliance:
    """Test README.md compliance with GATE 2 requirements."""
    
    @pytest.fixture
    def readme_content(self):
        """Load README.md content for testing."""
        readme_path = os.path.join(os.path.dirname(__file__), '..', 'README.md')
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def test_falcon_dataset_statement_present(self, readme_content):
        """Test that README contains explicit statement about Falcon dataset usage.
        
        Validates: Requirements 1.1
        """
        required_phrases = [
            "Falcon synthetic dataset",
            "exclusively",
            "Duality AI Space Station Challenge"
        ]
        
        for phrase in required_phrases:
            assert phrase in readme_content, f"README missing required phrase: '{phrase}'"
    
    def test_train_val_test_separation_documented(self, readme_content):
        """Test that README specifies strict train/val/test separation.
        
        Validates: Requirements 1.2
        """
        separation_indicators = [
            "strict train/val/test separation",
            "train/",
            "val/", 
            "test/"
        ]
        
        for indicator in separation_indicators:
            assert indicator in readme_content, f"README missing separation indicator: '{indicator}'"
    
    def test_challenge_context_referenced(self, readme_content):
        """Test that README references the Duality AI Space Station Challenge.
        
        Validates: Requirements 1.3
        """
        challenge_references = [
            "Duality AI Space Station Challenge",
            "challenge"
        ]
        
        # At least one challenge reference should be present
        assert any(ref in readme_content for ref in challenge_references), \
            "README missing Duality AI Space Station Challenge reference"
    
    def test_dataset_usage_discipline_section_exists(self, readme_content):
        """Test that README has a dedicated Dataset Usage Discipline section.
        
        Validates: Requirements 1.4 (partial - structure verification)
        """
        section_headers = [
            "Dataset Usage Discipline",
            "## 📋 Dataset Usage Discipline"
        ]
        
        assert any(header in readme_content for header in section_headers), \
            "README missing dedicated Dataset Usage Discipline section"
    
    def test_compliance_statement_present(self, readme_content):
        """Test that README contains a clear compliance statement.
        
        Validates: Requirements 1.1, 1.2
        """
        compliance_keywords = [
            "compliance",
            "exclusively",
            "no cross-contamination",
            "respective directories"
        ]
        
        # Should contain multiple compliance-related terms
        found_keywords = [kw for kw in compliance_keywords if kw in readme_content]
        assert len(found_keywords) >= 2, \
            f"README should contain more compliance keywords. Found: {found_keywords}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

import ast
import re
from hypothesis import given, strategies as st


class TestTrainingScriptCompliance:
    """Test training script compliance with GATE 2 path requirements."""
    
    @pytest.fixture
    def train_script_content(self):
        """Load src/train.py content for testing."""
        train_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'train.py')
        with open(train_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def test_no_hardcoded_paths_in_training_script(self, train_script_content):
        """Property 4: No hard-coded paths in training script.
        
        Feature: gate2-dataset-discipline, Property 4: No hard-coded paths in training script
        Validates: Requirements 2.4, 2.5
        """
        # Look for hard-coded path patterns
        hardcoded_patterns = [
            r'["\'][^"\']*data/raw[^"\']*["\']',  # Quoted paths containing data/raw
            r'["\'][^"\']*\.\.\/[^"\']*images[^"\']*["\']',  # Relative paths to images
            r'["\'][^"\']*\/.*\.jpg["\']',  # Direct image file paths
            r'["\'][^"\']*\/.*\.yaml["\']'  # Direct yaml file paths (except config)
        ]
        
        for pattern in hardcoded_patterns:
            matches = re.findall(pattern, train_script_content)
            # Filter out acceptable config references
            forbidden_matches = [m for m in matches if 'config/observo.yaml' not in m]
            assert not forbidden_matches, f"Found hard-coded paths: {forbidden_matches}"
    
    def test_uses_configuration_for_paths(self, train_script_content):
        """Property 4: Training script uses configuration files for all dataset path references.
        
        Feature: gate2-dataset-discipline, Property 4: No hard-coded paths in training script  
        Validates: Requirements 2.4, 2.5
        """
        # Should contain configuration loading functions
        required_functions = [
            'load_dataset_config',
            'validate_dataset_separation'
        ]
        
        for func in required_functions:
            assert func in train_script_content, f"Missing configuration function: {func}"
        
        # Should reference config file
        assert 'config/observo.yaml' in train_script_content, \
            "Training script should reference config/observo.yaml"
    
    @given(st.text(min_size=1, max_size=50))
    def test_path_isolation_property(self, phase_name):
        """Property 1: Training phase path isolation.
        
        Feature: gate2-dataset-discipline, Property 1: Training phase path isolation
        Validates: Requirements 2.1
        """
        # For any training phase, only appropriate directory should be referenced
        from src.train import load_dataset_config
        
        config = load_dataset_config()
        
        # Verify train/val/test directories are separate
        train_dir = config['train']
        val_dir = config['val'] 
        test_dir = config['test']
        
        # Property: directories should be distinct
        directories = [train_dir, val_dir, test_dir]
        assert len(set(directories)) == len(directories), \
            f"Directories must be separate: {directories}"
        
        # Property: each directory should be for its specific phase
        assert 'train' in train_dir.lower(), f"Train directory should contain 'train': {train_dir}"
        assert 'val' in val_dir.lower(), f"Val directory should contain 'val': {val_dir}"
        assert 'test' in test_dir.lower(), f"Test directory should contain 'test': {test_dir}"


class TestConfigurationCompliance:
    """Test configuration file compliance with GATE 2 requirements."""
    
    @pytest.fixture
    def config_content(self):
        """Load config/observo.yaml content for testing."""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'observo.yaml')
        with open(config_path, 'r', encoding='utf-8') as f:
            import yaml
            return yaml.safe_load(f)
    
    def test_configuration_structure_compliance(self, config_content):
        """Test presence of required train/val/test directories.
        
        Validates: Requirements 3.2
        """
        required_keys = ['train', 'val', 'test', 'path']
        
        for key in required_keys:
            assert key in config_content, f"Configuration missing required key: {key}"
    
    @given(st.text(min_size=1, max_size=100))
    def test_relative_paths_property(self, dummy_text):
        """Property 5: Configuration uses relative paths.
        
        Feature: gate2-dataset-discipline, Property 5: Configuration uses relative paths
        Validates: Requirements 3.1, 3.3
        """
        from src.train import load_dataset_config
        
        config = load_dataset_config()
        
        # Property: all paths should be relative (not absolute)
        path_keys = ['path', 'train', 'val', 'test']
        
        for key in path_keys:
            if key in config:
                path_value = config[key]
                # Property: should not start with / or C:\ (absolute path indicators)
                assert not os.path.isabs(path_value), \
                    f"Path '{key}': '{path_value}' should be relative, not absolute"


class TestDetectionScriptCompliance:
    """Test detection script compliance with GATE 2 path requirements."""
    
    @pytest.fixture
    def detect_script_content(self):
        """Load src/detect.py content for testing."""
        detect_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'detect.py')
        with open(detect_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def test_detection_uses_test_directory_only(self, detect_script_content):
        """Property 3: Test phase path isolation.
        
        Feature: gate2-dataset-discipline, Property 3: Test phase path isolation
        Validates: Requirements 2.3
        """
        # Should not contain hard-coded test paths
        hardcoded_test_patterns = [
            r'["\'][^"\']*data/raw/test[^"\']*["\']',
            r'["\'][^"\']*\.\.\/.*test.*images[^"\']*["\']'
        ]
        
        for pattern in hardcoded_test_patterns:
            matches = re.findall(pattern, detect_script_content)
            assert not matches, f"Found hard-coded test paths: {matches}"
        
        # Should use configuration-driven approach
        assert 'get_default_test_image' in detect_script_content, \
            "Detection script should use configuration-driven test image path"
        
        assert 'load_dataset_config' in detect_script_content, \
            "Detection script should load configuration for paths"
    
    @given(st.text(min_size=1, max_size=50))
    def test_test_phase_isolation_property(self, dummy_input):
        """Property 3: Test phase path isolation for detection operations.
        
        Feature: gate2-dataset-discipline, Property 3: Test phase path isolation
        Validates: Requirements 2.3
        """
        from src.detect import load_dataset_config, get_default_test_image
        
        config = load_dataset_config()
        test_image_path = get_default_test_image()
        
        # Property: test image path should reference test directory only
        assert config['test'] in test_image_path, \
            f"Test image path should reference test directory: {test_image_path}"
        
        # Property: should not reference train or val directories
        assert config['train'] not in test_image_path, \
            f"Test image path should not reference train directory: {test_image_path}"
        assert config['val'] not in test_image_path, \
            f"Test image path should not reference val directory: {test_image_path}"