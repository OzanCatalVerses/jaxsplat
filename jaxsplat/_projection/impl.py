from jax.interpreters import mlir, xla
from jax.lib import xla_client
from jax import core

import functools

from jaxsplat import _jaxsplat
from jaxsplat._projection import lowering, abstract


# register GPU XLA custom calls
for name, value in _jaxsplat.registrations().items():
    xla_client.register_custom_call_target(name, value, platform="gpu")


# forward
_project_gaussians_fwd_p = core.Primitive("project_gaussians_fwd")
_project_gaussians_fwd_p.multiple_results = True
_project_gaussians_fwd_p.def_impl(
    functools.partial(xla.apply_primitive, _project_gaussians_fwd_p)
)
_project_gaussians_fwd_p.def_abstract_eval(abstract._project_gaussians_fwd_abs)

mlir.register_lowering(
    prim=_project_gaussians_fwd_p,
    rule=lowering._project_gaussians_fwd_lowering,
    platform="gpu",
)

# backward
_project_gaussians_bwd_p = core.Primitive("project_gaussians_bwd")
_project_gaussians_bwd_p.multiple_results = True
_project_gaussians_bwd_p.def_impl(
    functools.partial(xla.apply_primitive, _project_gaussians_bwd_p)
)
_project_gaussians_bwd_p.def_abstract_eval(abstract._project_gaussians_bwd_abs)

mlir.register_lowering(
    prim=_project_gaussians_bwd_p,
    rule=lowering._project_gaussians_bwd_lowering,
    platform="gpu",
)
