// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: ds.proto

#define INTERNAL_SUPPRESS_PROTOBUF_FIELD_DEPRECATION
#include "ds.pb.h"

#include <algorithm>

#include <google/protobuf/stubs/common.h>
#include <google/protobuf/stubs/once.h>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/wire_format_lite_inl.h>
#include <google/protobuf/descriptor.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/reflection_ops.h>
#include <google/protobuf/wire_format.h>
// @@protoc_insertion_point(includes)

namespace stradsds {

namespace {

const ::google::protobuf::Descriptor* dshardctxmsg_descriptor_ = NULL;
const ::google::protobuf::internal::GeneratedMessageReflection*
  dshardctxmsg_reflection_ = NULL;
const ::google::protobuf::EnumDescriptor* matrix_type_descriptor_ = NULL;

}  // namespace


void protobuf_AssignDesc_ds_2eproto() {
  protobuf_AddDesc_ds_2eproto();
  const ::google::protobuf::FileDescriptor* file =
    ::google::protobuf::DescriptorPool::generated_pool()->FindFileByName(
      "ds.proto");
  GOOGLE_CHECK(file != NULL);
  dshardctxmsg_descriptor_ = file->message_type(0);
  static const int dshardctxmsg_offsets_[5] = {
    GOOGLE_PROTOBUF_GENERATED_MESSAGE_FIELD_OFFSET(dshardctxmsg, fn_),
    GOOGLE_PROTOBUF_GENERATED_MESSAGE_FIELD_OFFSET(dshardctxmsg, alias_),
    GOOGLE_PROTOBUF_GENERATED_MESSAGE_FIELD_OFFSET(dshardctxmsg, mtype_),
    GOOGLE_PROTOBUF_GENERATED_MESSAGE_FIELD_OFFSET(dshardctxmsg, m_maxrow_),
    GOOGLE_PROTOBUF_GENERATED_MESSAGE_FIELD_OFFSET(dshardctxmsg, m_maxcol_),
  };
  dshardctxmsg_reflection_ =
    new ::google::protobuf::internal::GeneratedMessageReflection(
      dshardctxmsg_descriptor_,
      dshardctxmsg::default_instance_,
      dshardctxmsg_offsets_,
      GOOGLE_PROTOBUF_GENERATED_MESSAGE_FIELD_OFFSET(dshardctxmsg, _has_bits_[0]),
      GOOGLE_PROTOBUF_GENERATED_MESSAGE_FIELD_OFFSET(dshardctxmsg, _unknown_fields_),
      -1,
      ::google::protobuf::DescriptorPool::generated_pool(),
      ::google::protobuf::MessageFactory::generated_factory(),
      sizeof(dshardctxmsg));
  matrix_type_descriptor_ = file->enum_type(0);
}

namespace {

GOOGLE_PROTOBUF_DECLARE_ONCE(protobuf_AssignDescriptors_once_);
inline void protobuf_AssignDescriptorsOnce() {
  ::google::protobuf::GoogleOnceInit(&protobuf_AssignDescriptors_once_,
                 &protobuf_AssignDesc_ds_2eproto);
}

void protobuf_RegisterTypes(const ::std::string&) {
  protobuf_AssignDescriptorsOnce();
  ::google::protobuf::MessageFactory::InternalRegisterGeneratedMessage(
    dshardctxmsg_descriptor_, &dshardctxmsg::default_instance());
}

}  // namespace

void protobuf_ShutdownFile_ds_2eproto() {
  delete dshardctxmsg::default_instance_;
  delete dshardctxmsg_reflection_;
}

void protobuf_AddDesc_ds_2eproto() {
  static bool already_here = false;
  if (already_here) return;
  already_here = true;
  GOOGLE_PROTOBUF_VERIFY_VERSION;

  ::google::protobuf::DescriptorPool::InternalAddGeneratedFile(
    "\n\010ds.proto\022\010stradsds\"s\n\014dshardctxmsg\022\n\n\002"
    "fn\030\001 \002(\t\022\r\n\005alias\030\002 \002(\t\022$\n\005mtype\030\003 \002(\0162\025"
    ".stradsds.matrix_type\022\020\n\010m_maxrow\030\004 \002(\004\022"
    "\020\n\010m_maxcol\030\005 \002(\004*J\n\013matrix_type\022\n\n\006cm_m"
    "ap\020\000\022\n\n\006cm_vec\020\001\022\n\n\006rm_map\020\002\022\n\n\006rm_vec\020\003"
    "\022\013\n\007dense2d\020\004", 213);
  ::google::protobuf::MessageFactory::InternalRegisterGeneratedFile(
    "ds.proto", &protobuf_RegisterTypes);
  dshardctxmsg::default_instance_ = new dshardctxmsg();
  dshardctxmsg::default_instance_->InitAsDefaultInstance();
  ::google::protobuf::internal::OnShutdown(&protobuf_ShutdownFile_ds_2eproto);
}

// Force AddDescriptors() to be called at static initialization time.
struct StaticDescriptorInitializer_ds_2eproto {
  StaticDescriptorInitializer_ds_2eproto() {
    protobuf_AddDesc_ds_2eproto();
  }
} static_descriptor_initializer_ds_2eproto_;
const ::google::protobuf::EnumDescriptor* matrix_type_descriptor() {
  protobuf_AssignDescriptorsOnce();
  return matrix_type_descriptor_;
}
bool matrix_type_IsValid(int value) {
  switch(value) {
    case 0:
    case 1:
    case 2:
    case 3:
    case 4:
      return true;
    default:
      return false;
  }
}


// ===================================================================

#ifndef _MSC_VER
const int dshardctxmsg::kFnFieldNumber;
const int dshardctxmsg::kAliasFieldNumber;
const int dshardctxmsg::kMtypeFieldNumber;
const int dshardctxmsg::kMMaxrowFieldNumber;
const int dshardctxmsg::kMMaxcolFieldNumber;
#endif  // !_MSC_VER

dshardctxmsg::dshardctxmsg()
  : ::google::protobuf::Message() {
  SharedCtor();
  // @@protoc_insertion_point(constructor:stradsds.dshardctxmsg)
}

void dshardctxmsg::InitAsDefaultInstance() {
}

dshardctxmsg::dshardctxmsg(const dshardctxmsg& from)
  : ::google::protobuf::Message() {
  SharedCtor();
  MergeFrom(from);
  // @@protoc_insertion_point(copy_constructor:stradsds.dshardctxmsg)
}

void dshardctxmsg::SharedCtor() {
  ::google::protobuf::internal::GetEmptyString();
  _cached_size_ = 0;
  fn_ = const_cast< ::std::string*>(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
  alias_ = const_cast< ::std::string*>(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
  mtype_ = 0;
  m_maxrow_ = GOOGLE_ULONGLONG(0);
  m_maxcol_ = GOOGLE_ULONGLONG(0);
  ::memset(_has_bits_, 0, sizeof(_has_bits_));
}

dshardctxmsg::~dshardctxmsg() {
  // @@protoc_insertion_point(destructor:stradsds.dshardctxmsg)
  SharedDtor();
}

void dshardctxmsg::SharedDtor() {
  if (fn_ != &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    delete fn_;
  }
  if (alias_ != &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    delete alias_;
  }
  if (this != default_instance_) {
  }
}

void dshardctxmsg::SetCachedSize(int size) const {
  GOOGLE_SAFE_CONCURRENT_WRITES_BEGIN();
  _cached_size_ = size;
  GOOGLE_SAFE_CONCURRENT_WRITES_END();
}
const ::google::protobuf::Descriptor* dshardctxmsg::descriptor() {
  protobuf_AssignDescriptorsOnce();
  return dshardctxmsg_descriptor_;
}

const dshardctxmsg& dshardctxmsg::default_instance() {
  if (default_instance_ == NULL) protobuf_AddDesc_ds_2eproto();
  return *default_instance_;
}

dshardctxmsg* dshardctxmsg::default_instance_ = NULL;

dshardctxmsg* dshardctxmsg::New() const {
  return new dshardctxmsg;
}

void dshardctxmsg::Clear() {
#define OFFSET_OF_FIELD_(f) (reinterpret_cast<char*>(      \
  &reinterpret_cast<dshardctxmsg*>(16)->f) - \
   reinterpret_cast<char*>(16))

#define ZR_(first, last) do {                              \
    size_t f = OFFSET_OF_FIELD_(first);                    \
    size_t n = OFFSET_OF_FIELD_(last) - f + sizeof(last);  \
    ::memset(&first, 0, n);                                \
  } while (0)

  if (_has_bits_[0 / 32] & 31) {
    ZR_(m_maxrow_, mtype_);
    if (has_fn()) {
      if (fn_ != &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
        fn_->clear();
      }
    }
    if (has_alias()) {
      if (alias_ != &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
        alias_->clear();
      }
    }
  }

#undef OFFSET_OF_FIELD_
#undef ZR_

  ::memset(_has_bits_, 0, sizeof(_has_bits_));
  mutable_unknown_fields()->Clear();
}

bool dshardctxmsg::MergePartialFromCodedStream(
    ::google::protobuf::io::CodedInputStream* input) {
#define DO_(EXPRESSION) if (!(EXPRESSION)) goto failure
  ::google::protobuf::uint32 tag;
  // @@protoc_insertion_point(parse_start:stradsds.dshardctxmsg)
  for (;;) {
    ::std::pair< ::google::protobuf::uint32, bool> p = input->ReadTagWithCutoff(127);
    tag = p.first;
    if (!p.second) goto handle_unusual;
    switch (::google::protobuf::internal::WireFormatLite::GetTagFieldNumber(tag)) {
      // required string fn = 1;
      case 1: {
        if (tag == 10) {
          DO_(::google::protobuf::internal::WireFormatLite::ReadString(
                input, this->mutable_fn()));
          ::google::protobuf::internal::WireFormat::VerifyUTF8StringNamedField(
            this->fn().data(), this->fn().length(),
            ::google::protobuf::internal::WireFormat::PARSE,
            "fn");
        } else {
          goto handle_unusual;
        }
        if (input->ExpectTag(18)) goto parse_alias;
        break;
      }

      // required string alias = 2;
      case 2: {
        if (tag == 18) {
         parse_alias:
          DO_(::google::protobuf::internal::WireFormatLite::ReadString(
                input, this->mutable_alias()));
          ::google::protobuf::internal::WireFormat::VerifyUTF8StringNamedField(
            this->alias().data(), this->alias().length(),
            ::google::protobuf::internal::WireFormat::PARSE,
            "alias");
        } else {
          goto handle_unusual;
        }
        if (input->ExpectTag(24)) goto parse_mtype;
        break;
      }

      // required .stradsds.matrix_type mtype = 3;
      case 3: {
        if (tag == 24) {
         parse_mtype:
          int value;
          DO_((::google::protobuf::internal::WireFormatLite::ReadPrimitive<
                   int, ::google::protobuf::internal::WireFormatLite::TYPE_ENUM>(
                 input, &value)));
          if (::stradsds::matrix_type_IsValid(value)) {
            set_mtype(static_cast< ::stradsds::matrix_type >(value));
          } else {
            mutable_unknown_fields()->AddVarint(3, value);
          }
        } else {
          goto handle_unusual;
        }
        if (input->ExpectTag(32)) goto parse_m_maxrow;
        break;
      }

      // required uint64 m_maxrow = 4;
      case 4: {
        if (tag == 32) {
         parse_m_maxrow:
          DO_((::google::protobuf::internal::WireFormatLite::ReadPrimitive<
                   ::google::protobuf::uint64, ::google::protobuf::internal::WireFormatLite::TYPE_UINT64>(
                 input, &m_maxrow_)));
          set_has_m_maxrow();
        } else {
          goto handle_unusual;
        }
        if (input->ExpectTag(40)) goto parse_m_maxcol;
        break;
      }

      // required uint64 m_maxcol = 5;
      case 5: {
        if (tag == 40) {
         parse_m_maxcol:
          DO_((::google::protobuf::internal::WireFormatLite::ReadPrimitive<
                   ::google::protobuf::uint64, ::google::protobuf::internal::WireFormatLite::TYPE_UINT64>(
                 input, &m_maxcol_)));
          set_has_m_maxcol();
        } else {
          goto handle_unusual;
        }
        if (input->ExpectAtEnd()) goto success;
        break;
      }

      default: {
      handle_unusual:
        if (tag == 0 ||
            ::google::protobuf::internal::WireFormatLite::GetTagWireType(tag) ==
            ::google::protobuf::internal::WireFormatLite::WIRETYPE_END_GROUP) {
          goto success;
        }
        DO_(::google::protobuf::internal::WireFormat::SkipField(
              input, tag, mutable_unknown_fields()));
        break;
      }
    }
  }
success:
  // @@protoc_insertion_point(parse_success:stradsds.dshardctxmsg)
  return true;
failure:
  // @@protoc_insertion_point(parse_failure:stradsds.dshardctxmsg)
  return false;
#undef DO_
}

void dshardctxmsg::SerializeWithCachedSizes(
    ::google::protobuf::io::CodedOutputStream* output) const {
  // @@protoc_insertion_point(serialize_start:stradsds.dshardctxmsg)
  // required string fn = 1;
  if (has_fn()) {
    ::google::protobuf::internal::WireFormat::VerifyUTF8StringNamedField(
      this->fn().data(), this->fn().length(),
      ::google::protobuf::internal::WireFormat::SERIALIZE,
      "fn");
    ::google::protobuf::internal::WireFormatLite::WriteStringMaybeAliased(
      1, this->fn(), output);
  }

  // required string alias = 2;
  if (has_alias()) {
    ::google::protobuf::internal::WireFormat::VerifyUTF8StringNamedField(
      this->alias().data(), this->alias().length(),
      ::google::protobuf::internal::WireFormat::SERIALIZE,
      "alias");
    ::google::protobuf::internal::WireFormatLite::WriteStringMaybeAliased(
      2, this->alias(), output);
  }

  // required .stradsds.matrix_type mtype = 3;
  if (has_mtype()) {
    ::google::protobuf::internal::WireFormatLite::WriteEnum(
      3, this->mtype(), output);
  }

  // required uint64 m_maxrow = 4;
  if (has_m_maxrow()) {
    ::google::protobuf::internal::WireFormatLite::WriteUInt64(4, this->m_maxrow(), output);
  }

  // required uint64 m_maxcol = 5;
  if (has_m_maxcol()) {
    ::google::protobuf::internal::WireFormatLite::WriteUInt64(5, this->m_maxcol(), output);
  }

  if (!unknown_fields().empty()) {
    ::google::protobuf::internal::WireFormat::SerializeUnknownFields(
        unknown_fields(), output);
  }
  // @@protoc_insertion_point(serialize_end:stradsds.dshardctxmsg)
}

::google::protobuf::uint8* dshardctxmsg::SerializeWithCachedSizesToArray(
    ::google::protobuf::uint8* target) const {
  // @@protoc_insertion_point(serialize_to_array_start:stradsds.dshardctxmsg)
  // required string fn = 1;
  if (has_fn()) {
    ::google::protobuf::internal::WireFormat::VerifyUTF8StringNamedField(
      this->fn().data(), this->fn().length(),
      ::google::protobuf::internal::WireFormat::SERIALIZE,
      "fn");
    target =
      ::google::protobuf::internal::WireFormatLite::WriteStringToArray(
        1, this->fn(), target);
  }

  // required string alias = 2;
  if (has_alias()) {
    ::google::protobuf::internal::WireFormat::VerifyUTF8StringNamedField(
      this->alias().data(), this->alias().length(),
      ::google::protobuf::internal::WireFormat::SERIALIZE,
      "alias");
    target =
      ::google::protobuf::internal::WireFormatLite::WriteStringToArray(
        2, this->alias(), target);
  }

  // required .stradsds.matrix_type mtype = 3;
  if (has_mtype()) {
    target = ::google::protobuf::internal::WireFormatLite::WriteEnumToArray(
      3, this->mtype(), target);
  }

  // required uint64 m_maxrow = 4;
  if (has_m_maxrow()) {
    target = ::google::protobuf::internal::WireFormatLite::WriteUInt64ToArray(4, this->m_maxrow(), target);
  }

  // required uint64 m_maxcol = 5;
  if (has_m_maxcol()) {
    target = ::google::protobuf::internal::WireFormatLite::WriteUInt64ToArray(5, this->m_maxcol(), target);
  }

  if (!unknown_fields().empty()) {
    target = ::google::protobuf::internal::WireFormat::SerializeUnknownFieldsToArray(
        unknown_fields(), target);
  }
  // @@protoc_insertion_point(serialize_to_array_end:stradsds.dshardctxmsg)
  return target;
}

int dshardctxmsg::ByteSize() const {
  int total_size = 0;

  if (_has_bits_[0 / 32] & (0xffu << (0 % 32))) {
    // required string fn = 1;
    if (has_fn()) {
      total_size += 1 +
        ::google::protobuf::internal::WireFormatLite::StringSize(
          this->fn());
    }

    // required string alias = 2;
    if (has_alias()) {
      total_size += 1 +
        ::google::protobuf::internal::WireFormatLite::StringSize(
          this->alias());
    }

    // required .stradsds.matrix_type mtype = 3;
    if (has_mtype()) {
      total_size += 1 +
        ::google::protobuf::internal::WireFormatLite::EnumSize(this->mtype());
    }

    // required uint64 m_maxrow = 4;
    if (has_m_maxrow()) {
      total_size += 1 +
        ::google::protobuf::internal::WireFormatLite::UInt64Size(
          this->m_maxrow());
    }

    // required uint64 m_maxcol = 5;
    if (has_m_maxcol()) {
      total_size += 1 +
        ::google::protobuf::internal::WireFormatLite::UInt64Size(
          this->m_maxcol());
    }

  }
  if (!unknown_fields().empty()) {
    total_size +=
      ::google::protobuf::internal::WireFormat::ComputeUnknownFieldsSize(
        unknown_fields());
  }
  GOOGLE_SAFE_CONCURRENT_WRITES_BEGIN();
  _cached_size_ = total_size;
  GOOGLE_SAFE_CONCURRENT_WRITES_END();
  return total_size;
}

void dshardctxmsg::MergeFrom(const ::google::protobuf::Message& from) {
  GOOGLE_CHECK_NE(&from, this);
  const dshardctxmsg* source =
    ::google::protobuf::internal::dynamic_cast_if_available<const dshardctxmsg*>(
      &from);
  if (source == NULL) {
    ::google::protobuf::internal::ReflectionOps::Merge(from, this);
  } else {
    MergeFrom(*source);
  }
}

void dshardctxmsg::MergeFrom(const dshardctxmsg& from) {
  GOOGLE_CHECK_NE(&from, this);
  if (from._has_bits_[0 / 32] & (0xffu << (0 % 32))) {
    if (from.has_fn()) {
      set_fn(from.fn());
    }
    if (from.has_alias()) {
      set_alias(from.alias());
    }
    if (from.has_mtype()) {
      set_mtype(from.mtype());
    }
    if (from.has_m_maxrow()) {
      set_m_maxrow(from.m_maxrow());
    }
    if (from.has_m_maxcol()) {
      set_m_maxcol(from.m_maxcol());
    }
  }
  mutable_unknown_fields()->MergeFrom(from.unknown_fields());
}

void dshardctxmsg::CopyFrom(const ::google::protobuf::Message& from) {
  if (&from == this) return;
  Clear();
  MergeFrom(from);
}

void dshardctxmsg::CopyFrom(const dshardctxmsg& from) {
  if (&from == this) return;
  Clear();
  MergeFrom(from);
}

bool dshardctxmsg::IsInitialized() const {
  if ((_has_bits_[0] & 0x0000001f) != 0x0000001f) return false;

  return true;
}

void dshardctxmsg::Swap(dshardctxmsg* other) {
  if (other != this) {
    std::swap(fn_, other->fn_);
    std::swap(alias_, other->alias_);
    std::swap(mtype_, other->mtype_);
    std::swap(m_maxrow_, other->m_maxrow_);
    std::swap(m_maxcol_, other->m_maxcol_);
    std::swap(_has_bits_[0], other->_has_bits_[0]);
    _unknown_fields_.Swap(&other->_unknown_fields_);
    std::swap(_cached_size_, other->_cached_size_);
  }
}

::google::protobuf::Metadata dshardctxmsg::GetMetadata() const {
  protobuf_AssignDescriptorsOnce();
  ::google::protobuf::Metadata metadata;
  metadata.descriptor = dshardctxmsg_descriptor_;
  metadata.reflection = dshardctxmsg_reflection_;
  return metadata;
}


// @@protoc_insertion_point(namespace_scope)

}  // namespace stradsds

// @@protoc_insertion_point(global_scope)
