# Design Document: GATE 2 Dataset Usage Discipline

## Overview

This design implements GATE 2 compliance by establishing proper dataset usage documentation, cleaning up hard-coded paths, and ensuring strict train/validation/test separation. The solution focuses on configuration-driven dataset management and comprehensive documentation to meet Duality AI Space Station Challenge requirements.

## Architecture

The compliance system consists of four main components:

1. **Documentation Layer**: Enhanced README.md with explicit dataset usage statements
2. **Configuration Management**: Centralized YAML-based dataset path configuration
3. **Training Script Compliance**: Updated training scripts that reference only approved paths
4. **Legacy Path Migration**: Systematic identification and deprecation of old path references

## Components and Interfaces

### Documentation Component

**README.md Enhancement**
- Location: Root directory
- Purpose: Provide explicit compliance statements
- Interface: Markdown documentation with dedicated dataset section

**Content Structure:**
```markdown
## Dataset Usage Discipline

This model was trained exclusively on the Falcon synthetic dataset provided for the Duality AI Space Station Challenge, with strict train/val/test separation.

### Dataset Structure
- Training: `train/` directory only
- Validation: `val/` directory only  
- Testing: `test/` directory only

### Compliance Statement
All training, validation, and testing operations reference only their respective directories with no cross-contamination or hard-coded paths.
```

### Configuration Management Component

**Primary Configuration: config/observo.yaml**
- Centralized dataset path definitions
- Relative path references only
- Clear train/val/test separation

**Configuration Schema:**
```yaml
# Dataset configuration for Falcon synthetic dataset
path: ../data/raw  # Base path to dataset
train: train/images  # Training images directory
val: val/images      # Validation images directory  
test: test/images    # Test images directory
nc: 3               # Number of classes
names: ['toolbox','oxygen_tank','fire_extinguisher']
```

### Training Script Component

**src/train.py Updates**
- Remove hard-coded paths
- Use configuration-driven path resolution
- Implement proper dataset separation validation

**Path Resolution Logic:**
```python
def load_dataset_config():
    """Load dataset configuration from approved config file"""
    config_path = os.path.join(os.path.dirname(__file__), '../config/observo.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def validate_dataset_separation(config):
    """Ensure train/val/test directories are properly separated"""
    required_dirs = ['train', 'val', 'test']
    for dir_type in required_dirs:
        if dir_type not in config:
            raise ValueError(f"Missing {dir_type} directory in configuration")
```

### Legacy Path Migration Component

**Deprecation Strategy**
- Identify all hard-coded paths in codebase
- Add deprecation warnings and comments
- Provide migration guidance
- Maintain backward compatibility during transition

## Data Models

### Configuration Model
```python
@dataclass
class DatasetConfig:
    path: str          # Base dataset path
    train: str         # Training directory
    val: str           # Validation directory  
    test: str          # Test directory
    nc: int           # Number of classes
    names: List[str]  # Class names
    
    def get_train_path(self) -> str:
        return os.path.join(self.path, self.train)
    
    def get_val_path(self) -> str:
        return os.path.join(self.path, self.val)
        
    def get_test_path(self) -> str:
        return os.path.join(self.path, self.test)
```

### Evidence Model
```python
@dataclass  
class ComplianceEvidence:
    readme_statement: str      # README compliance text
    config_snippet: str        # Configuration file content
    training_paths: List[str]  # Paths used in training script
    legacy_paths: List[str]    # Deprecated path references
    validation_results: Dict   # Compliance validation results
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Converting EARS to Properties

Based on the prework analysis, I'll convert the testable acceptance criteria into correctness properties:

**Property 1: Training phase path isolation**
*For any* training operation in the training script, only train/ directory paths should be referenced
**Validates: Requirements 2.1**

**Property 2: Validation phase path isolation**  
*For any* validation operation in the training script, only val/ directory paths should be referenced
**Validates: Requirements 2.2**

**Property 3: Test phase path isolation**
*For any* evaluation operation in the training script, only test/ directory paths should be referenced  
**Validates: Requirements 2.3**

**Property 4: No hard-coded paths in training script**
*For any* path reference in the training script, it should be resolved through configuration files rather than hard-coded
**Validates: Requirements 2.4, 2.5**

**Property 5: Configuration uses relative paths**
*For any* path definition in configuration files, it should use relative references rather than absolute paths
**Validates: Requirements 3.1, 3.3**

**Property 6: Legacy path deprecation**
*For any* legacy dataset path found in the codebase, it should be marked with deprecation comments
**Validates: Requirements 3.4, 4.1**

**Property 7: No active legacy path usage**
*For any* training or inference operation, legacy paths should not be actively used
**Validates: Requirements 4.3**

## Error Handling

### Configuration Validation Errors
- Missing required directories (train/val/test) in configuration
- Invalid path formats (absolute paths where relative expected)
- Inaccessible dataset directories

**Error Response Strategy:**
```python
class DatasetConfigError(Exception):
    """Raised when dataset configuration is invalid"""
    pass

def validate_config(config: DatasetConfig) -> None:
    """Validate dataset configuration compliance"""
    required_dirs = ['train', 'val', 'test']
    for dir_name in required_dirs:
        if not hasattr(config, dir_name):
            raise DatasetConfigError(f"Missing required directory: {dir_name}")
        
        path = getattr(config, dir_name)
        if os.path.isabs(path):
            raise DatasetConfigError(f"Absolute path not allowed: {path}")
```

### Legacy Path Detection
- Automated scanning for hard-coded paths
- Warning generation for deprecated references
- Migration guidance provision

### Evidence Generation Failures
- Handle missing files gracefully
- Provide partial evidence when complete evidence unavailable
- Clear error messages for compliance issues

## Testing Strategy

### Dual Testing Approach
The testing strategy combines unit tests for specific compliance checks with property-based tests for comprehensive validation across all configurations and code paths.

**Unit Tests:**
- Verify README contains required statements (Requirements 1.1, 1.2, 1.3)
- Check configuration file structure (Requirements 3.2)
- Validate evidence generation output (Requirements 5.1, 5.2, 5.3)
- Test specific examples of compliant vs non-compliant configurations

**Property-Based Tests:**
- Test path isolation properties across all training phases (Properties 1-3)
- Validate configuration compliance across all possible path formats (Properties 4-5)
- Verify legacy path handling across all code files (Properties 6-7)
- Generate random configurations and verify compliance rules hold

**Property Test Configuration:**
- Minimum 100 iterations per property test
- Each property test references its design document property
- Tag format: **Feature: gate2-dataset-discipline, Property {number}: {property_text}**

**Testing Framework:**
- Use pytest for unit tests
- Use Hypothesis for property-based testing in Python
- Each correctness property implemented as a single property-based test
- Tests validate universal properties across all valid inputs

**Integration Testing:**
- End-to-end compliance validation
- Evidence generation workflow testing
- Configuration migration testing
- Cross-platform path handling validation