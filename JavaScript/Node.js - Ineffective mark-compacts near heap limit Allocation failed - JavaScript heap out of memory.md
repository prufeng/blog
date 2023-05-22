编译打包Angular项目的时候，第一次遇到JavaScript heap out of memory。

在build的时候加上--max_old_space_size参数即可。

node --max_old_space_size=4089 node_modules/@angular/cli/bin/ng build --prod --aot --output-hashing=all --base-href ./ --configuration=dev

Error：

<--- JS stacktrace --->

FATAL ERROR: Ineffective mark-compacts near heap limit Allocation failed - JavaScript heap out of memory
 1: 00007FF621F1058F napi_wrap+109311
 2: 00007FF621EB52B6 v8::internal::OrderedHashTable<v8::internal::OrderedHashSet,1>::NumberOfElementsOffset+33302
 3: 00007FF621EB6086 node::OnFatalError+294
 4: 00007FF62278153E v8::Isolate::ReportExternalAllocationLimitReached+94
 5: 00007FF6227663BD v8::SharedArrayBuffer::Externalize+781
 6: 00007FF62261084C v8::internal::Heap::EphemeronKeyWriteBarrierFromCode+1516
 7: 00007FF62261BB8A v8::internal::Heap::ProtectUnprotectedMemoryChunks+1258
 8: 00007FF622618D39 v8::internal::Heap::PageFlagsAreConsistent+2457
 9: 00007FF62260D961 v8::internal::Heap::CollectGarbage+2033
10: 00007FF62260BB65 v8::internal::Heap::AllocateExternalBackingStore+1317
11: 00007FF622625E06 v8::internal::Factory::AllocateRaw+166
12: 00007FF622639824 v8::internal::FactoryBase<v8::internal::Factory>::NewFixedArrayWithFiller+84
13: 00007FF622639B23 v8::internal::FactoryBase<v8::internal::Factory>::NewFixedArrayWithMap+35
14: 00007FF622440C6C v8::internal::OrderedHashTable<v8::internal::OrderedHashMap,2>::Allocate+124
15: 00007FF62244346B v8::internal::OrderedHashTable<v8::internal::OrderedHashMap,2>::Rehash+59
16: 00007FF62244224A v8::internal::OrderedHashTable<v8::internal::OrderedHashMap,2>::EnsureGrowable+90
17: 00007FF622379737 v8::internal::interpreter::JumpTableTargetOffsets::iterator::operator=+122119
18: 00007FF622809EED v8::internal::SetupIsolateDelegate::SetupHeap+463949
19: 00007FF6227E53C8 v8::internal::SetupIsolateDelegate::SetupHeap+313640
20: 00007FF6227A28D2 v8::internal::SetupIsolateDelegate::SetupHeap+40498
21: 00007FF6227A28D2 v8::internal::SetupIsolateDelegate::SetupHeap+40498
22: 00007FF6227A28D2 v8::internal::SetupIsolateDelegate::SetupHeap+40498
23: 00007FF6227A28D2 v8::internal::SetupIsolateDelegate::SetupHeap+40498
24: 00007FF6227A28D2 v8::internal::SetupIsolateDelegate::SetupHeap+40498
25: 00007FF6227A28D2 v8::internal::SetupIsolateDelegate::SetupHeap+40498
26: 00007FF6227A28D2 v8::internal::SetupIsolateDelegate::SetupHeap+40498
27: 0000022741C1B187
npm ERR! code ELIFECYCLE
npm ERR! errno 134
