## SG Go

一个对 Plumber 的 SG IR 进行可视化的小工具，因为生成的 SG IR 是一个图结构，需要一个伸缩性强的工具来查看节点和连接关系。
SG GO 使用 Flask 结合 Gojs 插件，让 SG IR 呈现在网页上。

## 开始使用

你需要安装 SgGO 包，使用命令行工具 `sg_go` 来启动，

```shell
sg_go view sg.json
```

`sg.json` 文件是 Plumebr 生成的 SG IR 的 json 格式文件，在你使用 Plumber 时可以从输出目录获取。