# GATE 6 — Failure Case Analysis

Analyzed 5 failure cases:

## Case 1: space_helmet_misclassified.jpg
- **What Failed:** Space helmet misclassified as toolbox
- **Why:** Similar metallic appearance confused the model
- **Fix Attempted:** Added more diverse helmet training examples

## Case 2: debris_fragment_missed.jpg
- **What Failed:** Small debris fragment not detected
- **Why:** Object too small and low contrast
- **Fix Attempted:** Reduced confidence threshold, enhanced small object detection

## Case 3: communication_device_partial.jpg
- **What Failed:** Communication device only partially detected
- **Why:** Device partially occluded by equipment
- **Fix Attempted:** Added occlusion augmentation during training

## Case 4: loose_tool_false_positive.jpg
- **What Failed:** False positive detection of loose tool
- **Why:** Structural component misidentified as tool
- **Fix Attempted:** Added hard negative mining

## Case 5: oxygen_tank_orientation.jpg
- **What Failed:** Oxygen tank not detected in unusual orientation
- **Why:** Model trained primarily on upright tanks
- **Fix Attempted:** Added rotation augmentation

