# Technical Report — AgriDoc-OfflineAI

**Team ID:** agridoc-offline-team  
**Domain:** agriculture_ai  
**Model:** Phi-3-mini-4k-instruct-Q4_K_M

---

## Problem

Smallholder farmers across Africa suffer significant crop loss due to plant diseases (such as Cassava Mosaic and Cassava Brown Streak) but lack stable internet connectivity and expensive cloud infrastructure to access real-time agricultural expertise. This application addresses this challenge by providing a 100% offline, zero-cloud agricultural intelligence system designed specifically for low-end, commodity hardware in remote field conditions.

---

## Design Decisions

- **Base model:** Microsoft Phi-3-mini-4k-instruct (3.8B parameters) selected for superior reasoning capabilities on agricultural text data.
- **Quantization:** Q4_K_M quantization chosen for an optimal balance between output quality and memory footprint, fitting seamlessly within strict RAM constraints.
- **Alternatives considered:** Larger quantization levels (like Q8_0) exceeded the target 8 GB RAM limit, while ultra-low quantizations like Q2_K degraded text generation quality too aggressively for reliable farming guidance.

---

## Constraints

- Target hardware profile: Standard commodity laptops with 8 GB DDR4 RAM, integrated GPU, and Ubuntu 22.04.
- No GPU acceleration constraint — pure CPU inference via `llama.cpp` using optimized thread allocation (`n_threads=4`).
- Strict requirement for zero internet connectivity or cloud API dependencies in rural African farming regions.

---

## Benchmarks

| Metric | Value |
|---|---|
| Machine | Standard ADTC Evaluation Laptop Profile (i5/Ryzen 5, 8GB RAM) |
| RAM at peak | 3.2 GB |
| Time to first token | ~450 ms |
| Generation speed | ~16.5 t/s |
| Thermal throttling | None observed (CPU temperatures maintained safely below 72°C) |

These are self-reported development benchmarks. Official scores are measured by the ADTC profiler on the standard evaluation machine.
