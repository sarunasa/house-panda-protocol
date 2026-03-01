# NVIDIA DGX Spark — Coding Performance Analysis

_March 2026_

## Hardware Specifications

- **Superchip:** GB10 Grace Blackwell
- **CPU:** 20 ARM cores (10× Cortex-X925 performance, 10× Cortex-A725 efficiency)
- **GPU:** Up to 1 PFLOP FP4 sparse tensor performance (with structured sparsity)
- **Memory:** 128GB unified LPDDR5X, 273 GB/s bandwidth
- **Connectivity:** 2× QSFP ports (200 Gbps total via ConnectX-7), 10 GbE RJ-45, 4× USB-C (240W PD)
- **Form factor:** 129 × 150 × 50 mm (1.13L chassis)
- **Power:** 210W TDP (~105W typical load)
- **Price:** $3,999

## Real-World Token Generation Speeds

| Model | Quantization | Speed | Notes |
|-------|-------------|-------|-------|
| Llama 3.1 8B | FP4 | ~924 tok/s batch, ~36 tok/s chat | Small model, fast |
| Qwen3-Coder 30B | Q4 | 20-25 tok/s (16K ctx), 15-17 tok/s (32K ctx) | Primary coding model |
| GPT-OSS 120B | Q4 | ~59 tok/s gen, ~3,600 tok/s prefill | Large model, fits in 128GB |
| Llama 3.3 70B | QLoRA | 5,079 tok/s peak | Fine-tuning speed |

## Fine-Tuning Performance

| Model | Method | Speed |
|-------|--------|-------|
| Llama 3.2B | Full fine-tune | 82,739 tok/s |
| Llama 3.1 8B | LoRA | 53,657 tok/s |

## Critical Limitations

### 1. Memory Bandwidth Bottleneck
273 GB/s LPDDR5X vs 819 GB/s on Mac Studio M3 Ultra. This is THE limiting factor for token-intensive tasks. KV cache reads from memory slow down as context window fills.

### 2. Sparsity Dependency
Advertised 1 PFLOP requires structured sparsity (skipping zero-value operations). Dense compute drops to ~480 TFLOPS. Highly workload-dependent — real coding inference rarely hits theoretical peak.

### 3. Thermal Throttling
Compact 150mm chassis runs hot under sustained load. Some users report system reboots during extended workloads. January 2026 firmware update added 18W power savings when ConnectX-7 idle.

### 4. Single-User Token Speed
For interactive chatbot inference, tops out at 35-40 tok/s. Mac M4 Pro matches this at $1,400 vs $3,999. RTX 5090 reported 3-5x faster at ~$2,000.

## vs API Inference (Claude Sonnet 4.5)

| Factor | DGX Spark (Qwen3-Coder 30B) | Claude Sonnet API |
|--------|---------------------------|-------------------|
| Token generation | 20-25 tok/s | 80-120 tok/s sustained |
| Speed multiplier | 1× | **4-6× faster** |
| Context window | 16-32K practical | 200K |
| Model quality | Frontier for coding (80.2% SWE-Bench) | Frontier general + coding |
| Privacy | Complete — on-premises | Data sent to API provider |

**Verdict: API inference is significantly faster AND uses smarter models for interactive coding.**

## Where DGX Spark Wins

1. **Capacity over throughput** — Can hold 120B+ parameter models that crash 24GB GPUs. Unified 128GB enables models up to 200B parameters.
2. **Privacy/compliance** — Data stays on-premises. Critical for certain clients/projects.
3. **CUDA ecosystem** — Full NVIDIA stack preinstalled (CUDA, PyTorch, TensorRT, vLLM, SGLang).
4. **Dual-Spark clustering** — Two units connect via 200 Gbps QSFP. EXO Labs demo: Spark handles prefill, Mac Studio handles decode → 2.8× speedup vs Mac alone.
5. **Energy efficiency** — Most tokens per kWh among tested systems. 210W vs 1,050W for 3× RTX 3090.
6. **Concurrent models** — 128GB enables running multiple models simultaneously (e.g., GPT-OSS 20B + Qwen3-Coder 30B).

## Dual DGX Spark (2× units, $8K)

- 256GB total unified memory
- Qwen3 235B: 23,477 tok/s (prefill benchmark)
- Enables 200B+ parameter models unavailable on consumer hardware
- Still slower than API for <70B models in interactive coding

## Competitive Landscape

| System | Price | Memory BW | Token Gen | Ecosystem |
|--------|-------|-----------|-----------|----------|
| DGX Spark | $3,999 | 273 GB/s | 20-40 tok/s | CUDA (full stack) |
| Mac Studio M3 Ultra | ~$4,000 | 819 GB/s | Faster for inference | Metal/MLX |
| RTX 5090 | ~$2,000 | Higher | 3-5× faster | CUDA (consumer) |
| AMD Strix Halo | ~$2,000 | Comparable | Similar | ROCm (weaker ecosystem) |

## Conclusion for House Panda

DGX Spark is a **capacity and ecosystem play**, not a throughput champion. Value proposition is strongest when you need: CUDA compatibility, 128GB unified memory, RDMA networking, containerized workflows, or on-prem compliance. For pure coding speed, API inference remains 4-6× faster.

Best use: always-on inference infrastructure for protocol operations (bonding curve AI, MM monitoring, PVD signal processing) — not as a replacement for API-based development tools.
