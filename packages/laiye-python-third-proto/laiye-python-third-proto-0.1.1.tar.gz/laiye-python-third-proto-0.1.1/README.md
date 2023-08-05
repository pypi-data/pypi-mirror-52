# laiye-python-third-proto
laiye use third proto

## 用于第三方的所有的proto打包用于python
目前所需要的第三方有这些
- google/protobuf 
- google/api
- github.com/mwitkow/go-proto-validators
- github.com/envoyproxy/protoc-gen-validate/validate
- github.com/grpc-ecosystem/grpc-gateway/protoc-gen-swagger/options

## 需要添加在仓库中的有
- github.com/mwitkow/go-proto-validators
- github.com/envoyproxy/protoc-gen-validate/validate
- github.com/grpc-ecosystem/grpc-gateway/protoc-gen-swagger/options

其余两个在requirements安装如下
- protobuf==3.6.1
- google-api==0.1.12

## 生成第三方的proto的命令
```
docker run -ti -v `pwd`:/im-saas-msgs-protos -v `pwd`/pbout/python:/im-saas-protos-python registry.cn-beijing.aliyuncs.com/im-saas/protobuf:self-build-latest python /im-saas-msgs-protos/ci/compile/compile_python_test.py --conf=/im-saas-msgs-protos/ci/env/env_gitlab.json --thirdproto=thirdprotos
```
生成目录为pbout/python/thirdprotos

