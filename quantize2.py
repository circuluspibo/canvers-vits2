import onnx
from onnxruntime.quantization import quantize_dynamic, QuantType

model_fp32 = 'ko_base.onnx'
model_quant = 'ko_base_int8.onnx'
quantized_model = quantize_dynamic(model_fp32, model_quant)
