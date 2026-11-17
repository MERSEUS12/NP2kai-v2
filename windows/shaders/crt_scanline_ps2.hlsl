// NP2kai optional CRT post-process, Direct3D 9 / ps_2_0.
// EffectStrengths: x = RGB mask, y = vignette, z = curvature * 0.04, w = glow
sampler2D FrameSampler : register(s0);
float ScanlineStrength : register(c0);
float ScanPhaseScale : register(c1);      // half of the destination height
float4 EffectStrengths : register(c2);
float4 FrameSize : register(c3);          // width, height, 1/width, 1/height
float4 ImageAdjust : register(c4);         // x=contrast, y=brightness
struct PixelInput { float2 uv : TEXCOORD0; float2 scan_uv : TEXCOORD1; };
float4 main(PixelInput input) : COLOR0
{
    float2 centered = input.scan_uv * 2.0 - 1.0;
    float2 warped = input.uv + centered * dot(centered, centered) * EffectStrengths.z;
    float4 color = tex2D(FrameSampler, warped);
    color.rgb = saturate((color.rgb - 0.5) * ImageAdjust.x + 0.5 + ImageAdjust.y);
    float2 texel = FrameSize.zw * 2.0;
    if (EffectStrengths.w > 0.001)
    {
        float3 h0 = tex2D(FrameSampler, warped + float2(texel.x, 0.0)).rgb;
        float3 h1 = tex2D(FrameSampler, warped - float2(texel.x, 0.0)).rgb;
        float3 h2 = tex2D(FrameSampler, warped + float2(0.0, texel.y)).rgb;
        float3 h3 = tex2D(FrameSampler, warped - float2(0.0, texel.y)).rgb;
        float3 halo = max(max(h0, h1), max(h2, h3));
        float lit = dot(halo, float3(0.3333333, 0.3333333, 0.3333333));
        float soft = saturate((lit - 0.70) * 1.8);
        color.rgb = saturate(color.rgb + halo * soft * EffectStrengths.w * 0.5);
    }
    // One dark row every two, whatever the output scaling is.
    float phase = frac(input.scan_uv.y * ScanPhaseScale + 0.25);
    color.rgb *= 1.0 - ScanlineStrength * abs(phase * 2.0 - 1.0);
    // Slot mask: RGB triads every three pixels plus a thin horizontal gap.
    float x3 = frac(input.uv.x * FrameSize.x * 0.33333334) * 3.0;
    float3 mask = (x3 < 1.0) ? float3(1.60, 0.40, 0.40) :
        ((x3 < 2.0) ? float3(0.40, 1.60, 0.40) : float3(0.40, 0.40, 1.60));
    color.rgb *= lerp(float3(1.0, 1.0, 1.0), mask, EffectStrengths.x);
    color.rgb *= 1.0 - EffectStrengths.x * 0.35 * abs(phase * 2.0 - 1.0);
    // CRT glass edge falloff: preserve the center and fade smoothly to black at the edges.
    float edge = max(abs(centered.x), abs(centered.y));
    float edgeFade = saturate((edge - 0.72) / 0.28);
    edgeFade = edgeFade * edgeFade * (3.0 - 2.0 * edgeFade);
    color.rgb *= 1.0 - EffectStrengths.y * edgeFade;
    return color;
}
