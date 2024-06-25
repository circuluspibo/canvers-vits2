import onnx
from onnxconverter_common import float16

model = onnx.load("ko_base.onnx")
model_fp16 = float16.convert_float_to_float16(model)
onnx.save(model_fp16, "ko_base_fp16.onnx")
