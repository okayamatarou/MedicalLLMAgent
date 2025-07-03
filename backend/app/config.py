import os
from pathlib import Path
from typing import Dict, Any
from hydra import compose, initialize_config_dir
from omegaconf import DictConfig, OmegaConf
import logging

logger = logging.getLogger(__name__)

class ConfigManager:
    def __init__(self):
        self.config_dir = Path(__file__).parent.parent.parent / "configs"
        self.current_config: DictConfig = None
        self._initialize_hydra()
    
    def _initialize_hydra(self):
        """Initialize Hydra with the configs directory"""
        try:
            with initialize_config_dir(config_dir=str(self.config_dir.absolute()), version_base=None):
                self.current_config = compose(config_name="config")
            logger.info("Hydra configuration loaded successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Hydra: {e}")
            raise
    
    def get_config(self) -> DictConfig:
        """Get current configuration"""
        return self.current_config
    
    def update_config(self, overrides: Dict[str, Any]) -> DictConfig:
        """Update configuration with new values"""
        try:
            override_list = []
            for key, value in overrides.items():
                override_list.append(f"{key}={value}")
            
            with initialize_config_dir(config_dir=str(self.config_dir.absolute()), version_base=None):
                self.current_config = compose(config_name="config", overrides=override_list)
            
            logger.info(f"Configuration updated with overrides: {overrides}")
            return self.current_config
        except Exception as e:
            logger.error(f"Failed to update configuration: {e}")
            raise
    
    def get_available_models(self) -> list:
        """Get list of available model configurations"""
        model_dir = self.config_dir / "model"
        models = []
        for model_file in model_dir.glob("*.yaml"):
            models.append(model_file.stem)
        return models
    
    def get_available_prompts(self) -> list:
        """Get list of available prompt configurations"""
        prompt_dir = self.config_dir / "prompt"
        prompts = []
        for prompt_file in prompt_dir.glob("*.yaml"):
            prompts.append(prompt_file.stem)
        return prompts
    
    def get_available_ui_configs(self) -> list:
        """Get list of available UI configurations"""
        ui_dir = self.config_dir / "ui"
        ui_configs = []
        for ui_file in ui_dir.glob("*.yaml"):
            ui_configs.append(ui_file.stem)
        return ui_configs

config_manager = ConfigManager()
