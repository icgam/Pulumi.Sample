# Sample for App registration

The first time we deploy this with pulumi up, everything is all right but

Steps to reproduce

1. Run **pulumi up** with the current configuration
2. Accept the changes.
3. Update **main**.py line number 13 from **default_permissions()** to **all_permissions()**
4. Run pulumi up again and it throws the following exception.

## **Exception**

Previewing update (dev):
Type Name Plan Info
pulumi:pulumi:Stack sample_2-dev 26 messages

- ├─ azuread:index:Application SampleApp_3 API-dev update [diff: ~requiredResourceAccesses]
  +- ├─ azuread:index:ServicePrincipal SampleApp_3 API-dev - ServicePrincipal replace [diff: ~applicationId]
  └─ azuread:index:Application SampleApp_3 Web-dev 1 error

Diagnostics:
azuread:index:Application (SampleApp_3 Web-dev):
error: transport is closing

pulumi:pulumi:Stack (sample_2-dev):
panic: interface conversion: interface {} is string, not map[string]interface {}
goroutine 13 [running]:
github.com/hashicorp/terraform-plugin-sdk/helper/schema.SerializeResourceForHash(0xc000b52df0, 0x140e040, 0x19d6180, 0xc000109900)
/home/runner/go/pkg/mod/github.com/hashicorp/terraform-plugin-sdk@v1.7.0/helper/schema/serialize.go:92 +0x34f
github.com/hashicorp/terraform-plugin-sdk/helper/schema.HashResource.func1(0x140e040, 0x19d6180, 0x1b)
/home/runner/go/pkg/mod/github.com/hashicorp/terraform-plugin-sdk@v1.7.0/helper/schema/set.go:32 +0x6f
github.com/pulumi/pulumi-terraform-bridge/v2/pkg/tfbridge.visitPropertyValue(0xc00009eaa0, 0x18, 0xc0008ba420, 0x18, 0x13eda80, 0xc0009402e0, 0xc000253540, 0x0, 0x0, 0xc000b53258)
/home/runner/go/pkg/mod/github.com/pulumi/pulumi-terraform-bridge/v2@v2.7.3/pkg/tfbridge/diff.go:140 +0x55c
github.com/pulumi/pulumi-terraform-bridge/v2/pkg/tfbridge.doIgnoreChanges(0xc00019e3c0, 0xc00019f4a0, 0xc000952a20, 0xc000a0e420, 0x0, 0x0, 0x0, 0xc000940620)  
 /home/runner/go/pkg/mod/github.com/pulumi/pulumi-terraform-bridge/v2@v2.7.3/pkg/tfbridge/diff.go:281 +0x3e2
github.com/pulumi/pulumi-terraform-bridge/v2/pkg/tfbridge.(*Provider).Diff(0xc0005f8700, 0x1a26fc0, 0xc000952990, 0xc000134150, 0xc0005f8700, 0x14aa401, 0xc000295500)
/home/runner/go/pkg/mod/github.com/pulumi/pulumi-terraform-bridge/v2@v2.7.3/pkg/tfbridge/provider.go:703 +0x7cc
github.com/pulumi/pulumi/sdk/v2/proto/go.\_ResourceProvider_Diff_Handler.func1(0x1a26fc0, 0xc000952990, 0x1601f00, 0xc000134150, 0x1610c60, 0x2561db0, 0x1a26fc0, 0xc000952990)
/home/runner/go/pkg/mod/github.com/pulumi/pulumi/sdk/v2@v2.9.1-0.20200825190708-910aa96016cd/proto/go/provider.pb.go:1866 +0x8d
github.com/grpc-ecosystem/grpc-opentracing/go/otgrpc.OpenTracingServerInterceptor.func1(0x1a26fc0, 0xc000757fb0, 0x1601f00, 0xc000134150, 0xc00041a100, 0xc00041a120, 0x0, 0x0, 0x19fe4a0, 0xc0001a0010)
/home/runner/go/pkg/mod/github.com/grpc-ecosystem/grpc-opentracing@v0.0.0-20180507213350-8e809c8a8645/go/otgrpc/server.go:57 +0x2f2
github.com/pulumi/pulumi/sdk/v2/proto/go.\_ResourceProvider_Diff_Handler(0x1638660, 0xc0005f8700, 0x1a26fc0, 0xc000757fb0, 0xc0008ced80, 0xc00024e3e0, 0x1a26fc0, 0xc000757fb0, 0xc00001e600, 0x100e)
/home/runner/go/pkg/mod/github.com/pulumi/pulumi/sdk/v2@v2.9.1-0.20200825190708-910aa96016cd/proto/go/provider.pb.go:1868 +0x152
google.golang.org/grpc.(*Server).processUnaryRPC(0xc00027e340, 0x1a374e0, 0xc00050c780, 0xc000904100, 0xc00019f920, 0x2521e30, 0x0, 0x0, 0x0)
/home/runner/go/pkg/mod/google.golang.org/grpc@v1.29.1/server.go:1082 +0x511
google.golang.org/grpc.(*Server).handleStream(0xc00027e340, 0x1a374e0, 0xc00050c780, 0xc000904100, 0x0)
/home/runner/go/pkg/mod/google.golang.org/grpc@v1.29.1/server.go:1405 +0xcd4
google.golang.org/grpc.(*Server).serveStreams.func1.1(0xc0002cdba0, 0xc00027e340, 0x1a374e0, 0xc00050c780, 0xc000904100)
/home/runner/go/pkg/mod/google.golang.org/grpc@v1.29.1/server.go:746 +0xa8
created by google.golang.org/grpc.(\*Server).serveStreams.func1
/home/runner/go/pkg/mod/google.golang.org/grpc@v1.29.1/server.go:744 +0xa8
