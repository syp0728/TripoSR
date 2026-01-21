from typing import Callable, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
# from torchmcubes import marching_cubes

# 6번째 줄 근처 (기존 주석 처리한 곳 아래에 추가)
try:
    from torchmcubes import marching_cubes
except ImportError:
    # torchmcubes가 없을 때 대신 사용할 함수를 정의합니다.
    from skimage.measure import marching_cubes


class IsosurfaceHelper(nn.Module):
    points_range: Tuple[float, float] = (0, 1)

    @property
    def grid_vertices(self) -> torch.FloatTensor:
        raise NotImplementedError


class MarchingCubeHelper(IsosurfaceHelper):
    def __init__(self, resolution: int) -> None:
        super().__init__()
        self.resolution = resolution
        self.mc_func: Callable = marching_cubes
        self._grid_vertices: Optional[torch.FloatTensor] = None

    @property
    def grid_vertices(self) -> torch.FloatTensor:
        if self._grid_vertices is None:
            # keep the vertices on CPU so that we can support very large resolution
            x, y, z = (
                torch.linspace(*self.points_range, self.resolution),
                torch.linspace(*self.points_range, self.resolution),
                torch.linspace(*self.points_range, self.resolution),
            )
            x, y, z = torch.meshgrid(x, y, z, indexing="ij")
            verts = torch.cat(
                [x.reshape(-1, 1), y.reshape(-1, 1), z.reshape(-1, 1)], dim=-1
            ).reshape(-1, 3)
            self._grid_vertices = verts
        return self._grid_vertices

    def forward(
        self,
        level: torch.FloatTensor,
    ) -> Tuple[torch.FloatTensor, torch.LongTensor]:
        level = -level.view(self.resolution, self.resolution, self.resolution)
        try:
            # v_pos, t_pos_idx = self.mc_func(level.detach(), 0.0)
            # 데이터를 넘파이 배열로 변환하여 전달합니다.
            v_pos, t_pos_idx, normals, values = self.mc_func(level.detach().cpu().numpy(), 0.0)
            # 결과값 중 필요한 정점(v_pos)과 면(t_pos_idx) 정보를 다시 텐서로 바꿉니다.
            import torch
            v_pos = torch.from_numpy(v_pos.copy()).to(level.device)
            t_pos_idx = torch.from_numpy(t_pos_idx.copy()).long().to(level.device)
        except AttributeError:
            print("torchmcubes was not compiled with CUDA support, use CPU version instead.")
            v_pos, t_pos_idx = self.mc_func(level.detach().cpu(), 0.0)
        v_pos = v_pos[..., [2, 1, 0]]
        v_pos = v_pos / (self.resolution - 1.0)
        return v_pos.to(level.device), t_pos_idx.to(level.device)
