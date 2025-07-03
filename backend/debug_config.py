from app.config import config_manager

def debug_config():
    print("=== Configuration Debug ===")
    config = config_manager.get_config()
    
    print("Full config structure:")
    print(f"Type: {type(config)}")
    print(f"Config: {config}")
    
    print("\nModel config:")
    print(f"Type: {type(config.model)}")
    print(f"Model: {config.model}")
    
    print("\nTrying to access model.model:")
    try:
        model_model = config.model.model
        print(f"Success - Type: {type(model_model)}")
        print(f"Content: {model_model}")
        print(f"Model type: {model_model.get('type', 'NOT_FOUND')}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\nTrying direct model access:")
    try:
        model_type = config.model.get("type", "NOT_FOUND")
        print(f"Direct model type: {model_type}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_config()
