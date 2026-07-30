from src.inference.model_loader import ModelLoader

loader = ModelLoader()

models = loader.load_models()

print("\nLoaded Models")

for antibiotic in loader.get_antibiotics():
    print(f"✓ {antibiotic}")

print()

print("Number of models :", len(models))

print("Features :", len(loader.get_feature_names()))