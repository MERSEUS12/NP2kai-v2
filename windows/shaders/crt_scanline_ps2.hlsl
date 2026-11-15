// NP2kai optional CRT post-process, Direct3D 9 / ps_2_0.
// This source is compiled at runtime by the optional CRT renderer.
// If compilation or shader creation fails, NP2kai must bypass the effect.
sampler2D FrameSampler : register(s0);

float ScanlineStrength : register(c0);
float PixelHeight : register(c1);

struct PixelInput
{
    float2 uv : TEXCOORD0;
};

float4 main(PixelInput input) : COLOR0
{
    float4 color = tex2D(FrameSampler, input.uv);

    // One dark trough per source scanline, with a smooth transition.
    // PixelHeight is the source image height in texels.
    float line = input.uv.y * PixelHeight;
    float phase = frac(line);
    float scan = 1.0 - ScanlineStrength * (0.5 - 0.5 * cos(phase * 6.2831853));

    color.rgb *= scan;
    return color;
}
