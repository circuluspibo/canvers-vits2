import onnx
from onnxruntime.quantization import quantize_dynamic, QuantType

model_fp32 = 'ko_emo.onnx'
model_quant = 'ko_emo_int8.onnx'
quantized_model = quantize_dynamic(model_fp32, model_quant,weight_type=QuantType.QInt8)

model_quant = 'ko_emo_uint8.onnx'
quantized_model = quantize_dynamic(model_fp32,  model_quant,weight_type=QuantType.QUInt8)
