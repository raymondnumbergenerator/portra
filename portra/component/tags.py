###
# Adobe Camera Raw parameters used in Adobe Lightroom and their default values.
###
LR_WHITE_BALANCE = {
    'Temperature': 6200,
    'Tint': 2,
    'WhiteBalance': 'As Shot'}
LR_TONE = {
    'Blacks2012': 0,
    'Contrast2012': 0,
    'Exposure2012': 0,
    'Highlights2012': 0,
    'Shadows2012': 0,
    'Whites2012': 0,
    'Clarity2012': 0}
LR_TONE_CURVE = {
    'ParametricDarks': 0,
    'ParametricHighlightSplit': 75,
    'ParametricHightlights': 0,
    'ParametricLights': 0,
    'ParametricMidtoneSplit': 50,
    'ParametricShadowSplit': 25,
    'ParametricShadows': 0,
    'ToneCurveName2012': 'Linear',
    'ToneCurvePV2012': '{0, 0, 255, 255,}',
    'ToneCurvePV2012Blue': '{0, 0, 255, 255,}',
    'ToneCurvePV2012Green': '{0, 0, 255, 255,}',
    'ToneCurvePV2012Red': '{0, 0, 255, 255,}'}
LR_COLOR = {
    'ConvertToGrayscale': 'false',
    'EnableColorAdjustments': 'true',
    'Saturation': 0,
    'Vibrance': 0}
LR_COLOR_ADJUSTMENTS = {
    'HueAdjustmentAqua': 0,
    'HueAdjustmentBlue': 0,
    'HueAdjustmentGreen': 0,
    'HueAdjustmentMagenta': 0,
    'HueAdjustmentOrange': 0,
    'HueAdjustmentPurple': 0,
    'HueAdjustmentRed': 0,
    'HueAdjustmentYellow': 0,
    'LuminanceAdjustmentAqua': 0,
    'LuminanceAdjustmentBlue': 0,
    'LuminanceAdjustmentGreen': 0,
    'LuminanceAdjustmentMagenta': 0,
    'LuminanceAdjustmentOrange': 0,
    'LuminanceAdjustmentPurple': 0,
    'LuminanceAdjustmentRed': 0,
    'LuminanceAdjustmentYellow': 0,
    'SaturationAdjustmentAqua': 0,
    'SaturationAdjustmentBlue': 0,
    'SaturationAdjustmentGreen': 0,
    'SaturationAdjustmentMagenta': 0,
    'SaturationAdjustmentOrange': 0,
    'SaturationAdjustmentPurple': 0,
    'SaturationAdjustmentRed': 0,
    'SaturationAdjustmentYellow': 0}
LR_SHARPENING = {
    'EnableDetail': 'true',
    'SharpenDetail': 25,
    'SharpenEdgeMasking': 0,
    'SharpenRadius': 1,
    'Sharpness': 25}
LR_EFFECTS = {
    'Dehaze': 0,
    'EnableEffects': 'true'}
LR_EFFECTS_GRAIN = {
    'GrainAmount': 0,
    'GrainFrequency': 50,
    'GrainSize': 25}
LR_EFFECTS_VIGNETTE = {
    'PostCropVignetteAmount': 0,
    'PostCropVignetteFeather': 50,
    'PostCropVignetteHighlightContrast': 0,
    'PostCropVignetteMidpoint': 50,
    'PostCropVignetteRoundness': 0,
    'PostCropVignetteStyle': 1}
LR_SPLIT_TONING = {
    'EnableSplitToning': 'true', 'SplitToningBalance': 0,
    'SplitToningHighlightHue': 0, 'SplitToningHighlightSaturation': 0,
    'SplitToningShadowHue': 0, 'SplitToningShadowSaturation': 0}
LR_DETAIL = {
    'EnableDetail': 'true'}
LR_DETAIL_LUMINANCE = {
    'LuminanceNoiseReductionContrast': 0,
    'LuminanceNoiseReductionDetail': 50,
    'LuminanceSmoothing': 0}
LR_DETAIL_COLOR = {
    'ColorNoiseReduction': 25,
    'ColorNoiseReductionDetail': 50,
    'ColorNoiseReductionSmoothness': 50}
LR_PROCESS_VERSION = {'ProcessVersion': '6.7'}
LR_CAMERA_CALIBRATION = {
    'CameraProfile': 'Adobe Standard',
    'EnableCalibration': 'true',
    'ShadowTint': 0,
    'RedHue': 0, 'RedSaturation': 0,
    'GreenHue': 0, 'GreenSaturation': 0,
    'BlueHue': 0, 'BlueSaturation': 0}

### Adobe Camera Raw Tone Curve settings that are stored as strings.
TC_TAGS_STRING = ['Version', 'ToneCurveName', 'ToneCurveName2012', 'HasSettings']
### Adobe Camera Raw Tone Curve settings that are stored as arrays.
TC_TAGS_ARRAY = ['ToneCurve', 'ToneCurveRed', 'ToneCurveGreen', 'ToneCurveBlue',
    'ToneCurvePV2012', 'ToneCurvePV2012Red', 'ToneCurvePV2012Green', 'ToneCurvePV2012Blue']
