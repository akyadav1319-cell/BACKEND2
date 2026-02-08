"""
Urban Impact Image Generator
Uses Stable Diffusion via Hugging Face Diffusers for before/after visualizations
"""

import os
import io
import base64
from PIL import Image
import torch
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline
from diffusers import DPMSolverMultistepScheduler
import numpy as np


class UrbanImpactGenerator:
    """
    Generates urban landscape before/after comparisons based on climate policies
    """

    def __init__(self):
        """Initialize Stable Diffusion models"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_id = "runwayml/stable-diffusion-v1-5"  # Free model

        # Initialize text-to-image pipeline
        print(f"🎨 Loading Stable Diffusion on {self.device}...")
        self.txt2img_pipe = StableDiffusionPipeline.from_pretrained(
            self.model_id,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            safety_checker=None,  # Disable for government use case
            requires_safety_checker=False
        )
        self.txt2img_pipe = self.txt2img_pipe.to(self.device)

        # Use DPM++ scheduler for faster generation
        self.txt2img_pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            self.txt2img_pipe.scheduler.config
        )

        # Initialize image-to-image pipeline (for baseline modification)
        self.img2img_pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
            self.model_id,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            safety_checker=None,
            requires_safety_checker=False
        )
        self.img2img_pipe = self.img2img_pipe.to(self.device)
        self.img2img_pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            self.img2img_pipe.scheduler.config
        )

        # Enable memory optimization
        if self.device == "cuda":
            self.txt2img_pipe.enable_attention_slicing()
            self.img2img_pipe.enable_attention_slicing()

        print("✅ Stable Diffusion models loaded successfully!")

    def _build_baseline_prompt(self, city_description, style):
        """Build prompt for baseline (current state) image"""
        base_prompt = f"{city_description}, "

        # Current state descriptors
        base_prompt += "pollution, smog, traffic congestion, diesel vehicles, "
        base_prompt += "industrial smokestacks, gray skies, carbon emissions, "
        base_prompt += "urban sprawl, asphalt parking lots, "

        # Style modifiers
        if style == "photorealistic":
            base_prompt += "photorealistic, detailed, professional photography, 4K, high resolution"
        else:
            base_prompt += "digital art, concept art, dramatic lighting, cinematic"

        return base_prompt

    def _build_impact_prompt(self, city_description, policy_inputs, calculation_result, style):
        """Build prompt for impact (transformed) image based on policies"""
        impact_prompt = f"{city_description}, "

        # Analyze which policies are implemented
        ev_level = policy_inputs.get("ev_adoption", 0)
        renewable_level = policy_inputs.get("renewable_energy", 0)
        carbon_tax_level = policy_inputs.get("carbon_tax", 0)
        reforestation_level = policy_inputs.get("reforestation", 0)
        public_transport_level = policy_inputs.get("public_transport", 0)
        industrial_controls_level = policy_inputs.get("industrial_controls", 0)
        green_buildings_level = policy_inputs.get("green_buildings", 0)
        waste_management_level = policy_inputs.get("waste_management", 0)

        # Build transformation descriptors based on policy levels
        transformations = []

        if ev_level > 50:
            transformations.append("electric vehicles everywhere")
            transformations.append("charging stations")
        if ev_level > 30:
            transformations.append("silent clean streets")

        if renewable_level > 50:
            transformations.append("solar panels on rooftops")
            transformations.append("wind turbines in distance")
        if renewable_level > 70:
            transformations.append("solar farms visible")

        if reforestation_level > 40:
            transformations.append("green parks")
            transformations.append("trees lining streets")
        if reforestation_level > 70:
            transformations.append("urban forest")
            transformations.append("rooftop gardens")

        if public_transport_level > 50:
            transformations.append("modern tram systems")
            transformations.append("bike lanes")
        if public_transport_level > 70:
            transformations.append("elevated metro")

        if industrial_controls_level > 50:
            transformations.append("clean industrial areas")
            transformations.append("no smoke from factories")

        if green_buildings_level > 50:
            transformations.append("green building facades")
            transformations.append("vertical gardens")
        if green_buildings_level > 70:
            transformations.append("eco-architecture")

        if waste_management_level > 50:
            transformations.append("clean streets")
            transformations.append("recycling infrastructure")

        # Add environmental improvements
        temp_mitigation = abs(calculation_result.get("temperature_mitigation", 0))
        if temp_mitigation > 0.2:
            transformations.append("clear blue skies")
            transformations.append("visible sunshine")
        if temp_mitigation > 0.4:
            transformations.append("pristine air quality")
            transformations.append("vibrant colors")

        # Combine all transformations
        impact_prompt += ", ".join(transformations[:10])  # Limit to 10 for prompt length

        # Add negative prompts (what to avoid)
        impact_prompt += ", sustainable future city, clean energy, eco-friendly, "

        # Style modifiers
        if style == "photorealistic":
            impact_prompt += "photorealistic, detailed, professional photography, 4K, high resolution"
        else:
            impact_prompt += "digital art, concept art, dramatic lighting, cinematic, hopeful atmosphere"

        return impact_prompt

    def _build_negative_prompt(self, is_baseline=True):
        """Build negative prompts to avoid undesired elements"""
        if is_baseline:
            # For baseline, avoid utopian elements
            return "clean, green, solar panels, wind turbines, trees, parks, electric cars, utopian"
        else:
            # For impact, avoid dystopian elements
            return "pollution, smog, smoke, dirty, gray, industrial waste, traffic jam, dystopian, dark"

    def _image_to_base64(self, image):
        """Convert PIL Image to base64 string"""
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str

    def _base64_to_image(self, base64_str):
        """Convert base64 string to PIL Image"""
        img_data = base64.b64decode(base64_str)
        image = Image.open(io.BytesIO(img_data))
        return image

    def generate_comparison(
            self,
            policy_inputs,
            calculation_result,
            city_description="modern urban cityscape",
            style="photorealistic",
            baseline_image_b64=None
    ):
        """
        Generate before/after comparison images

        Args:
            policy_inputs: Dict of policy levels (0-100)
            calculation_result: Output from PolicyEngine.calculate_impacts()
            city_description: Base description of the city
            style: "photorealistic" or "artistic"
            baseline_image_b64: Optional base64 encoded baseline image

        Returns:
            Dict with baseline_image, impact_image (base64), and description
        """
        # Generate or use provided baseline
        if baseline_image_b64:
            baseline_image = self._base64_to_image(baseline_image_b64)
        else:
            # Generate baseline from scratch
            baseline_prompt = self._build_baseline_prompt(city_description, style)
            baseline_negative = self._build_negative_prompt(is_baseline=True)

            print(f"🎨 Generating baseline image...")
            print(f"   Prompt: {baseline_prompt[:100]}...")

            baseline_image = self.txt2img_pipe(
                prompt=baseline_prompt,
                negative_prompt=baseline_negative,
                num_inference_steps=25,  # Balanced quality/speed
                guidance_scale=7.5,
                width=768,
                height=512
            ).images[0]

        # Generate impact image using img2img for consistency
        impact_prompt = self._build_impact_prompt(
            city_description,
            policy_inputs,
            calculation_result,
            style
        )
        impact_negative = self._build_negative_prompt(is_baseline=False)

        print(f"🎨 Generating impact image...")
        print(f"   Prompt: {impact_prompt[:100]}...")

        # Resize baseline to match expected dimensions
        baseline_resized = baseline_image.resize((768, 512))

        impact_image = self.img2img_pipe(
            prompt=impact_prompt,
            negative_prompt=impact_negative,
            image=baseline_resized,
            strength=0.75,  # How much to transform (0.75 = significant change)
            num_inference_steps=30,
            guidance_scale=8.0
        ).images[0]

        # Convert to base64
        baseline_b64 = self._image_to_base64(baseline_image)
        impact_b64 = self._image_to_base64(impact_image)

        # Generate description
        description = self._generate_description(policy_inputs, calculation_result)

        return {
            "baseline_image": baseline_b64,
            "impact_image": impact_b64,
            "description": description,
            "metadata": {
                "baseline_prompt": baseline_prompt if not baseline_image_b64 else "User provided",
                "impact_prompt": impact_prompt,
                "temperature_mitigation": calculation_result.get("temperature_mitigation_formatted"),
                "total_cost": calculation_result.get("total_cost_formatted")
            }
        }

    def quick_generate(self, policy_inputs, calculation_result, scenario="modern_city"):
        """
        Quick generation with predefined scenarios

        Args:
            policy_inputs: Dict of policy levels
            calculation_result: Engine output
            scenario: "coastal_city", "industrial_city", "suburban", "megacity"

        Returns:
            Same as generate_comparison
        """
        # Scenario templates
        scenarios = {
            "coastal_city": "coastal metropolitan city with harbor, ocean view, skyscrapers by the waterfront",
            "industrial_city": "industrial city with factories, manufacturing districts, port facilities",
            "suburban": "suburban town with residential areas, shopping districts, highways",
            "megacity": "massive megacity with dense skyscrapers, elevated highways, urban density",
            "modern_city": "modern city skyline with downtown district, parks, mixed-use development"
        }

        city_description = scenarios.get(scenario, scenarios["modern_city"])

        return self.generate_comparison(
            policy_inputs=policy_inputs,
            calculation_result=calculation_result,
            city_description=city_description,
            style="photorealistic",
            baseline_image_b64=None
        )

    def _generate_description(self, policy_inputs, calculation_result):
        """Generate textual description of the transformation"""
        active_policies = []

        for policy_key, level in policy_inputs.items():
            if level > 50:
                policy_name = policy_key.replace("_", " ").title()
                active_policies.append(f"{policy_name} ({level}%)")

        temp_impact = calculation_result.get("temperature_mitigation_formatted", "N/A")
        cost = calculation_result.get("total_cost_formatted", "N/A")

        description = f"Urban transformation visualization showing the impact of "
        description += f"{len(active_policies)} major climate policies: "
        description += ", ".join(active_policies[:3])
        if len(active_policies) > 3:
            description += f", and {len(active_policies) - 3} more"
        description += f". Projected temperature mitigation: {temp_impact}, "
        description += f"Total investment: {cost}."

        return description