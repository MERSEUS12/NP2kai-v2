// NP2kai optional CRT post-process, Direct3D 9 / ps_2_0.
// The renderer embeds this shader source and compiles it at runtime.
// If compilation or shader creation fails, NP2kai bypasses the effect and
// retains its fixed-function geometry scanline fallback.
sampler2D FrameSampler : register(s0);

float ScanlineStrength : register(c0);
float PixelHeight : register(c1);

struct PixelInput
{
    float2 uv : TEXCOORD0;
    float2 scan_uv : TEXCOORD1;
};

float4 main(PixelInput input) : COLOR0
{
    float4 color = tex2D(FrameSampler, input.uv);
    float phase = frac(input.scan_uv.y * PixelHeight);
    float scan = 1.0 - ScanlineStrength * (0.5 - 0.5 * cos(phase * 6.2831853));
    color.rgb *= scan;
    return color;
}
