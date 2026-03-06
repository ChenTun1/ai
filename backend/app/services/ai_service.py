"""
AI 图像生成服务 - 硅基流动 (SiliconFlow)

封装硅基流动 API，提供宠物旅行照片的 AI 生成能力。
"""

import httpx
from typing import Optional
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from loguru import logger

from app.core.config import settings
from app.models.pet import Pet
from app.models.location import Location


# 季节描述映射
SEASON_MAP: dict[str, str] = {
    "spring": "in spring with cherry blossoms and fresh green leaves",
    "summer": "in summer with bright sunshine and lush vegetation",
    "autumn": "in autumn with golden leaves and warm colors",
    "winter": "in winter with snow-covered scenery",
}

# 时间描述映射
TIME_OF_DAY_MAP: dict[str, str] = {
    "sunrise": "during sunrise with soft golden light",
    "noon": "at noon with bright natural lighting",
    "sunset": "during sunset with warm orange and pink sky",
    "night": "at night with city lights and starry sky",
}

# 风格描述映射
STYLE_MAP: dict[str, str] = {
    "realistic": "ultra realistic, photorealistic, 8k, high detail, professional photography",
    "pixel": "pixel art style, retro game aesthetic, 16-bit, vibrant colors",
    "anime": "anime style, Studio Ghibli inspired, vibrant colors, detailed illustration",
}


class AIImageService:
    """硅基流动 AI 图像生成服务。

    提供基于 Stable Diffusion XL 的宠物旅行照片生成功能，
    支持多种风格、季节和时间设定。

    Attributes:
        api_url: 硅基流动 API 地址
        api_key: API 密钥
        model: 使用的模型名称
        timeout: 请求超时时间（秒）
        max_retries: 最大重试次数
    """

    def __init__(self) -> None:
        self.api_url: str = settings.SILICONFLOW_API_URL
        self.api_key: str = settings.SILICONFLOW_API_KEY
        self.model: str = settings.AI_DEFAULT_MODEL
        self.timeout: int = settings.AI_TIMEOUT_SECONDS
        self.max_retries: int = settings.AI_MAX_RETRIES

    def build_prompt(
        self,
        pet: Pet,
        location: Location,
        style: str = "realistic",
        season: Optional[str] = None,
        time_of_day: Optional[str] = None,
    ) -> str:
        """构建图像生成的 Prompt。

        将宠物、地点、风格、季节、时间等信息组合成结构化的英文 Prompt。

        Args:
            pet: 宠物模型实例
            location: 地点模型实例
            style: 图像风格，可选 realistic / pixel / anime
            season: 季节，可选 spring / summer / autumn / winter
            time_of_day: 时间段，可选 sunrise / noon / sunset / night

        Returns:
            组合后的英文 Prompt 字符串
        """
        # 宠物描述
        if pet.ai_description:
            pet_desc = pet.ai_description
        else:
            breed = pet.breed or ""
            pet_desc = f"a {breed} {pet.type}".strip()

        # 地点描述
        location_desc = location.prompt_template or f"at {location.name_en}"

        # 组合 Prompt 各部分
        parts = [pet_desc, location_desc]

        if season and season in SEASON_MAP:
            parts.append(SEASON_MAP[season])

        if time_of_day and time_of_day in TIME_OF_DAY_MAP:
            parts.append(TIME_OF_DAY_MAP[time_of_day])

        # 风格放在最后作为修饰
        style_desc = STYLE_MAP.get(style, STYLE_MAP["realistic"])
        parts.append(style_desc)

        prompt = ", ".join(parts)
        logger.info(f"Built prompt: {prompt}")
        return prompt

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.ConnectError)),
        before_sleep=lambda retry_state: logger.warning(
            f"Retrying AI image generation (attempt {retry_state.attempt_number})..."
        ),
    )
    async def generate_image(
        self,
        prompt: str,
        style: str = "realistic",
        num_outputs: int = 1,
    ) -> list[str]:
        """调用硅基流动 API 生成图片。

        Args:
            prompt: 图像生成的文本描述
            style: 图像风格，用于确定推理步数等参数
            num_outputs: 生成图片数量，默认 1

        Returns:
            生成的图片 URL 列表

        Raises:
            httpx.HTTPStatusError: API 返回非 2xx 状态码
            httpx.ConnectError: 网络连接失败
            ValueError: API key 未配置
        """
        if not self.api_key:
            raise ValueError(
                "SILICONFLOW_API_KEY is not configured. "
                "Please set it in your .env file."
            )

        # 根据风格调整推理步数
        inference_steps = 30 if style == "realistic" else 20

        payload = {
            "model": self.model,
            "prompt": prompt,
            "image_size": "1024x1024",
            "num_inference_steps": inference_steps,
            "batch_size": num_outputs,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        logger.info(f"Calling SiliconFlow API with model={self.model}, batch_size={num_outputs}")

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                self.api_url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()

        result = response.json()
        image_urls: list[str] = [
            img["url"] for img in result.get("images", []) if img.get("url")
        ]

        logger.info(f"Generated {len(image_urls)} image(s) successfully")
        return image_urls


# 全局服务实例
ai_image_service = AIImageService()
