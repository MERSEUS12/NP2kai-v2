// NP2kai optional CRT post-process, Direct3D 9 / ps_2_0.
// Secondary effects are independently controlled and default to zero.
sampler2D FrameSampler : register(s0);
float ScanlineStrength : register(c0);
float PixelHeight : register(c1);
float4 EffectStrengths : register(c2); // RGB mask, vignette, curvature, glow
float4 FrameSize : register(c3);       // width, height, 1/width, 1/height
struct PixelInput { float2 uv : TEXCOORD0; float2 scan_uv : TEXCOORD1; };
float4 main(PixelInput input) : COLOR0
{
    float2 centered = input.scan_uv * 2.0 - 1.0;
    float curve = EffectStrengths.z * 0.08;
    float2 warped = input.uv + centered * dot(centered, centered) * curve * 0.5;
    float4 color = tex2D(FrameSampler, warped);
    float2 texel = FrameSize.zw;
    if (EffectStrengths.w > 0.001)
    {
        float3 glow = tex2D(FrameSampler, warped + float2(texel.x, 0.0)).rgb;
        glow += tex2D(FrameSampler, warped - float2(texel.x, 0.0)).rgb;
        glow += tex2D(FrameSampler, warped + float2(0.0, texel.y)).rgb;
        glow += tex2D(FrameSampler, warped - float2(0.0, texel.y)).rgb;
        color.rgb = lerp(color.rgb, max(color.rgb, glow * 0.25), EffectStrengths.w);
    }
    float phase = frac(input.scan_uv.y * PixelHeight);
    float scan = 1.0 - ScanlineStrength * (0.5 - 0.5 * cos(phase * 6.2831853));
    color.rgb *= scan;
    float stripe = fmod(floor(input.uv.x * FrameSize.x), 3.0);
    float3 mask = (stripe < 1.0) ? float3(1.0, 0.72, 0.72) :
        ((stripe < 2.0) ? float3(0.72, 1.0, 0.72) : float3(0.72, 0.72, 1.0));
    color.rgb *= lerp(float3(1.0, 1.0, 1.0), mask, EffectStrengths.x);
    float vignette = saturate(1.0 - dot(centered, centered) * EffectStrengths.y);
    color.rgb *= vignette;
    return color;
}
