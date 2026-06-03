# 流程树

```text
/start
  -> 说明 skill 定位、输入要求、命令清单

/intake
  -> 是否有 source video
     -> 否: 停止并要求补充原始视频
     -> 是: 建立 project brief 和 project manifest
  -> 是否有 subject / scene / prop / style assets
     -> 不完整: 记录缺口并允许继续，但标记风险

/ingest
  -> 读取视频元数据
  -> 判断画幅、帧率、时长、镜头运动类型
  -> 输出 video ingest card

/keyframes
  -> 是否已有现成关键帧
     -> 是: 规范命名并建立索引
     -> 否: 抽取 Anchor / Motion / Transition frames
  -> 输出 keyframe table 和 contact sheet

/diagnose
  -> 对每个核心帧输出 frame diagnosis card
  -> 若透视或接触点不明
     -> 标记 preprocess escalation

/assets
  -> 整理 subject / scene / prop / style bible
  -> 对 scene assets 生成 camera cards

/match
  -> frame 与 scene camera library 匹配评分
  -> score >= 80
     -> direct_fuse
  -> score 60-79
     -> empty_plate_first
  -> score < 60
     -> new_camera_needed

/preprocess
  -> 生成 required layer checklist
  -> 确认 mask / depth / pose / edge / contact outputs

/plate
  -> 如果结果为 empty_plate_first
     -> 先输出 empty plate prompt / plate asset spec
  -> 如果结果为 new_camera_needed
     -> 停止直接融合，要求新机位或新场景资产

/fusion
  -> 基于 structure + subject + environment 输出融合提示词
  -> 输出 repair prompt

/qc
  -> 检查 identity / outfit / prop / contact / perspective / relight / continuity
  -> 不通过
     -> 回退到 /match 或 /preprocess 或 /plate
  -> 通过
     -> 进入 /deliver

/deliver
  -> 汇总 manifests、QC 报告、最终交付摘要
  -> 标记项目完成状态
```
