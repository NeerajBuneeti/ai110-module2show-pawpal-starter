#!/usr/bin/env python3
"""
Test script for Challenge 2: Data Persistence
Demonstrates JSON serialization and deserialization of Owner data
"""

import json
import os
from pawpal_system import Owner, Pet, Task
from datetime import date

print("=" * 60)
print("Challenge 2: Data Persistence Test")
print("=" * 60)

# Create sample owner with multiple pets and tasks
print("\n1. Creating sample owner data...")
owner = Owner(name="Alice", available_time_per_day=240)

# Add dog with tasks
dog = Pet(name="Max", pet_type="dog", age=3)
dog.add_task(Task(name="Morning walk", duration=30, priority=5, category="walk", pet_id="Max", frequency="daily"))
dog.add_task(Task(name="Dog feeding", duration=10, priority=5, category="feeding", pet_id="Max", frequency="daily"))
dog.add_task(Task(name="Playtime", duration=20, priority=3, category="play", pet_id="Max", frequency="daily"))
owner.add_pet(dog)

# Add cat with tasks
cat = Pet(name="Whiskers", pet_type="cat", age=5)
cat.add_task(Task(name="Cat feeding", duration=8, priority=4, category="feeding", pet_id="Whiskers", frequency="daily"))
cat.add_task(Task(name="Litter box cleanup", duration=10, priority=4, category="litter", pet_id="Whiskers", frequency="daily"))
owner.add_pet(cat)

print(f"   ✓ Created owner: {owner.name}")
print(f"   ✓ Added {len(owner.pets)} pets: {[p.name for p in owner.pets]}")
print(f"   ✓ Added {len(owner.get_all_tasks())} tasks")

# Test serialization
print("\n2. Testing serialization to JSON...")
owner_dict = owner.to_dict()
print("   ✓ to_dict() successful")

# Save to file
filename = "test_data.json"
with open(filename, "w") as f:
    json.dump(owner_dict, f, indent=2)
print(f"   ✓ Saved to {filename}")

# Check file size
file_size = os.path.getsize(filename)
print(f"   ✓ File size: {file_size} bytes")

# Display JSON structure
print(f"\n   Sample JSON structure:")
print(f"   {json.dumps(owner_dict, indent=2)[:300]}...")

# Test deserialization
print("\n3. Testing deserialization from JSON...")
with open(filename, "r") as f:
    loaded_dict = json.load(f)
print("   ✓ Loaded JSON from file")

owner_restored = Owner.from_dict(loaded_dict)
print(f"   ✓ from_dict() successful")

# Verify data integrity
print(f"\n4. Verifying data integrity...")
print(f"   Owner name: {owner_restored.name} {'✓' if owner_restored.name == owner.name else '✗'}")
print(f"   Available time: {owner_restored.available_time_per_day} {'✓' if owner_restored.available_time_per_day == owner.available_time_per_day else '✗'}")
print(f"   Pet count: {len(owner_restored.pets)} {'✓' if len(owner_restored.pets) == len(owner.pets) else '✗'}")
print(f"   Task count: {len(owner_restored.get_all_tasks())} {'✓' if len(owner_restored.get_all_tasks()) == len(owner.get_all_tasks()) else '✗'}")

# Verify pet details
for i, (original_pet, restored_pet) in enumerate(zip(owner.pets, owner_restored.pets)):
    print(f"\n   Pet {i+1}: {restored_pet.name}")
    print(f"     Type: {restored_pet.pet_type} {'✓' if restored_pet.pet_type == original_pet.pet_type else '✗'}")
    print(f"     Age: {restored_pet.age} {'✓' if restored_pet.age == original_pet.age else '✗'}")
    print(f"     Tasks: {len(restored_pet.tasks)} {'✓' if len(restored_pet.tasks) == len(original_pet.tasks) else '✗'}")
    
    for j, (orig_task, rest_task) in enumerate(zip(original_pet.tasks, restored_pet.tasks)):
        match = (orig_task.name == rest_task.name and 
                orig_task.priority == rest_task.priority and
                orig_task.duration == rest_task.duration)
        status = "✓" if match else "✗"
        print(f"       Task {j+1}: {rest_task.name} (P:{rest_task.priority}, D:{rest_task.duration}m) {status}")

# Test round-trip
print("\n5. Testing round-trip serialization...")
owner_dict2 = owner_restored.to_dict()
assert owner_dict == owner_dict2, "Round-trip serialization failed!"
print("   ✓ Round-trip serialization verified")

# Cleanup
os.remove(filename)
print(f"   ✓ Cleaned up {filename}")

print("\n" + "=" * 60)
print("✅ All data persistence tests passed!")
print("=" * 60)
print("\nPawPal+ now persists pets and tasks to data.json between runs!")
