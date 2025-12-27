# Requirements Document

## Introduction

This specification defines the requirements for achieving GATE 2 — Dataset Usage Discipline compliance for the VISTA-S project. The goal is to ensure proper dataset usage documentation and eliminate hard-coded paths while maintaining strict train/validation/test separation as required by the Duality AI Space Station Challenge.

## Glossary

- **GATE 2**: Dataset Usage Discipline compliance requirement for the Duality AI Space Station Challenge
- **Falcon_Dataset**: The synthetic dataset provided specifically for the Duality AI Space Station Challenge
- **Training_Script**: The main training script (src/train.py) that handles model training
- **Configuration_File**: YAML files that define dataset paths and training parameters
- **Legacy_Path**: Any hard-coded or outdated dataset path reference that needs to be marked as deprecated

## Requirements

### Requirement 1: README Documentation

**User Story:** As a challenge evaluator, I want to see explicit documentation of dataset usage, so that I can verify compliance with challenge rules.

#### Acceptance Criteria

1. THE README.md SHALL contain an explicit statement about exclusive use of the Falcon synthetic dataset
2. THE README.md SHALL specify that the model was trained with strict train/val/test separation
3. THE README.md SHALL reference the Duality AI Space Station Challenge context
4. THE statement SHALL be prominently placed in a dedicated section

### Requirement 2: Training Script Compliance

**User Story:** As a developer, I want the training script to reference only approved dataset paths, so that I can ensure proper dataset separation.

#### Acceptance Criteria

1. THE Training_Script SHALL reference only train/ directory during training phases
2. THE Training_Script SHALL reference only val/ directory during validation phases  
3. THE Training_Script SHALL reference only test/ directory during evaluation phases
4. THE Training_Script SHALL NOT contain hard-coded image paths
5. THE Training_Script SHALL use configuration files for all dataset path references

### Requirement 3: Configuration Management

**User Story:** As a system administrator, I want clean configuration management, so that I can easily maintain and audit dataset usage.

#### Acceptance Criteria

1. THE Configuration_File SHALL define dataset paths using relative references
2. THE Configuration_File SHALL specify separate train, val, and test directories
3. THE Configuration_File SHALL NOT contain absolute or hard-coded paths
4. WHEN legacy configurations exist, THE system SHALL mark them as deprecated with clear comments

### Requirement 4: Legacy Path Cleanup

**User Story:** As a maintainer, I want legacy dataset references clearly identified, so that I can avoid confusion and ensure compliance.

#### Acceptance Criteria

1. WHEN legacy dataset paths are found, THE system SHALL mark them with deprecation comments
2. THE system SHALL provide clear migration guidance for any legacy references
3. THE system SHALL NOT use legacy paths in active training or inference
4. THE documentation SHALL explain the transition from legacy to compliant paths

### Requirement 5: Evidence Generation

**User Story:** As a challenge submitter, I want to generate proof of compliance, so that I can demonstrate adherence to GATE 2 requirements.

#### Acceptance Criteria

1. THE system SHALL provide screenshot-ready evidence of compliant dataset paths in training scripts
2. THE system SHALL generate a compliance summary showing proper train/val/test separation
3. THE evidence SHALL include relevant code snippets demonstrating proper configuration usage
4. THE evidence SHALL be easily accessible for challenge submission