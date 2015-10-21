// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: ds.proto

#ifndef PROTOBUF_ds_2eproto__INCLUDED
#define PROTOBUF_ds_2eproto__INCLUDED

#include <string>

#include <google/protobuf/stubs/common.h>

#if GOOGLE_PROTOBUF_VERSION < 2006000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers.  Please update
#error your headers.
#endif
#if 2006000 < GOOGLE_PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers.  Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>
#include <google/protobuf/extension_set.h>
#include <google/protobuf/generated_enum_reflection.h>
#include <google/protobuf/unknown_field_set.h>
// @@protoc_insertion_point(includes)

namespace stradsds {

// Internal implementation detail -- do not call these.
void  protobuf_AddDesc_ds_2eproto();
void protobuf_AssignDesc_ds_2eproto();
void protobuf_ShutdownFile_ds_2eproto();

class dshardctxmsg;

enum matrix_type {
  cm_map = 0,
  cm_vec = 1,
  rm_map = 2,
  rm_vec = 3,
  dense2d = 4
};
bool matrix_type_IsValid(int value);
const matrix_type matrix_type_MIN = cm_map;
const matrix_type matrix_type_MAX = dense2d;
const int matrix_type_ARRAYSIZE = matrix_type_MAX + 1;

const ::google::protobuf::EnumDescriptor* matrix_type_descriptor();
inline const ::std::string& matrix_type_Name(matrix_type value) {
  return ::google::protobuf::internal::NameOfEnum(
    matrix_type_descriptor(), value);
}
inline bool matrix_type_Parse(
    const ::std::string& name, matrix_type* value) {
  return ::google::protobuf::internal::ParseNamedEnum<matrix_type>(
    matrix_type_descriptor(), name, value);
}
// ===================================================================

class dshardctxmsg : public ::google::protobuf::Message {
 public:
  dshardctxmsg();
  virtual ~dshardctxmsg();

  dshardctxmsg(const dshardctxmsg& from);

  inline dshardctxmsg& operator=(const dshardctxmsg& from) {
    CopyFrom(from);
    return *this;
  }

  inline const ::google::protobuf::UnknownFieldSet& unknown_fields() const {
    return _unknown_fields_;
  }

  inline ::google::protobuf::UnknownFieldSet* mutable_unknown_fields() {
    return &_unknown_fields_;
  }

  static const ::google::protobuf::Descriptor* descriptor();
  static const dshardctxmsg& default_instance();

  void Swap(dshardctxmsg* other);

  // implements Message ----------------------------------------------

  dshardctxmsg* New() const;
  void CopyFrom(const ::google::protobuf::Message& from);
  void MergeFrom(const ::google::protobuf::Message& from);
  void CopyFrom(const dshardctxmsg& from);
  void MergeFrom(const dshardctxmsg& from);
  void Clear();
  bool IsInitialized() const;

  int ByteSize() const;
  bool MergePartialFromCodedStream(
      ::google::protobuf::io::CodedInputStream* input);
  void SerializeWithCachedSizes(
      ::google::protobuf::io::CodedOutputStream* output) const;
  ::google::protobuf::uint8* SerializeWithCachedSizesToArray(::google::protobuf::uint8* output) const;
  int GetCachedSize() const { return _cached_size_; }
  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const;
  public:
  ::google::protobuf::Metadata GetMetadata() const;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  // required string fn = 1;
  inline bool has_fn() const;
  inline void clear_fn();
  static const int kFnFieldNumber = 1;
  inline const ::std::string& fn() const;
  inline void set_fn(const ::std::string& value);
  inline void set_fn(const char* value);
  inline void set_fn(const char* value, size_t size);
  inline ::std::string* mutable_fn();
  inline ::std::string* release_fn();
  inline void set_allocated_fn(::std::string* fn);

  // required string alias = 2;
  inline bool has_alias() const;
  inline void clear_alias();
  static const int kAliasFieldNumber = 2;
  inline const ::std::string& alias() const;
  inline void set_alias(const ::std::string& value);
  inline void set_alias(const char* value);
  inline void set_alias(const char* value, size_t size);
  inline ::std::string* mutable_alias();
  inline ::std::string* release_alias();
  inline void set_allocated_alias(::std::string* alias);

  // required .stradsds.matrix_type mtype = 3;
  inline bool has_mtype() const;
  inline void clear_mtype();
  static const int kMtypeFieldNumber = 3;
  inline ::stradsds::matrix_type mtype() const;
  inline void set_mtype(::stradsds::matrix_type value);

  // required uint64 m_maxrow = 4;
  inline bool has_m_maxrow() const;
  inline void clear_m_maxrow();
  static const int kMMaxrowFieldNumber = 4;
  inline ::google::protobuf::uint64 m_maxrow() const;
  inline void set_m_maxrow(::google::protobuf::uint64 value);

  // required uint64 m_maxcol = 5;
  inline bool has_m_maxcol() const;
  inline void clear_m_maxcol();
  static const int kMMaxcolFieldNumber = 5;
  inline ::google::protobuf::uint64 m_maxcol() const;
  inline void set_m_maxcol(::google::protobuf::uint64 value);

  // @@protoc_insertion_point(class_scope:stradsds.dshardctxmsg)
 private:
  inline void set_has_fn();
  inline void clear_has_fn();
  inline void set_has_alias();
  inline void clear_has_alias();
  inline void set_has_mtype();
  inline void clear_has_mtype();
  inline void set_has_m_maxrow();
  inline void clear_has_m_maxrow();
  inline void set_has_m_maxcol();
  inline void clear_has_m_maxcol();

  ::google::protobuf::UnknownFieldSet _unknown_fields_;

  ::google::protobuf::uint32 _has_bits_[1];
  mutable int _cached_size_;
  ::std::string* fn_;
  ::std::string* alias_;
  ::google::protobuf::uint64 m_maxrow_;
  ::google::protobuf::uint64 m_maxcol_;
  int mtype_;
  friend void  protobuf_AddDesc_ds_2eproto();
  friend void protobuf_AssignDesc_ds_2eproto();
  friend void protobuf_ShutdownFile_ds_2eproto();

  void InitAsDefaultInstance();
  static dshardctxmsg* default_instance_;
};
// ===================================================================


// ===================================================================

// dshardctxmsg

// required string fn = 1;
inline bool dshardctxmsg::has_fn() const {
  return (_has_bits_[0] & 0x00000001u) != 0;
}
inline void dshardctxmsg::set_has_fn() {
  _has_bits_[0] |= 0x00000001u;
}
inline void dshardctxmsg::clear_has_fn() {
  _has_bits_[0] &= ~0x00000001u;
}
inline void dshardctxmsg::clear_fn() {
  if (fn_ != &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    fn_->clear();
  }
  clear_has_fn();
}
inline const ::std::string& dshardctxmsg::fn() const {
  // @@protoc_insertion_point(field_get:stradsds.dshardctxmsg.fn)
  return *fn_;
}
inline void dshardctxmsg::set_fn(const ::std::string& value) {
  set_has_fn();
  if (fn_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    fn_ = new ::std::string;
  }
  fn_->assign(value);
  // @@protoc_insertion_point(field_set:stradsds.dshardctxmsg.fn)
}
inline void dshardctxmsg::set_fn(const char* value) {
  set_has_fn();
  if (fn_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    fn_ = new ::std::string;
  }
  fn_->assign(value);
  // @@protoc_insertion_point(field_set_char:stradsds.dshardctxmsg.fn)
}
inline void dshardctxmsg::set_fn(const char* value, size_t size) {
  set_has_fn();
  if (fn_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    fn_ = new ::std::string;
  }
  fn_->assign(reinterpret_cast<const char*>(value), size);
  // @@protoc_insertion_point(field_set_pointer:stradsds.dshardctxmsg.fn)
}
inline ::std::string* dshardctxmsg::mutable_fn() {
  set_has_fn();
  if (fn_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    fn_ = new ::std::string;
  }
  // @@protoc_insertion_point(field_mutable:stradsds.dshardctxmsg.fn)
  return fn_;
}
inline ::std::string* dshardctxmsg::release_fn() {
  clear_has_fn();
  if (fn_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    return NULL;
  } else {
    ::std::string* temp = fn_;
    fn_ = const_cast< ::std::string*>(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
    return temp;
  }
}
inline void dshardctxmsg::set_allocated_fn(::std::string* fn) {
  if (fn_ != &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    delete fn_;
  }
  if (fn) {
    set_has_fn();
    fn_ = fn;
  } else {
    clear_has_fn();
    fn_ = const_cast< ::std::string*>(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
  }
  // @@protoc_insertion_point(field_set_allocated:stradsds.dshardctxmsg.fn)
}

// required string alias = 2;
inline bool dshardctxmsg::has_alias() const {
  return (_has_bits_[0] & 0x00000002u) != 0;
}
inline void dshardctxmsg::set_has_alias() {
  _has_bits_[0] |= 0x00000002u;
}
inline void dshardctxmsg::clear_has_alias() {
  _has_bits_[0] &= ~0x00000002u;
}
inline void dshardctxmsg::clear_alias() {
  if (alias_ != &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    alias_->clear();
  }
  clear_has_alias();
}
inline const ::std::string& dshardctxmsg::alias() const {
  // @@protoc_insertion_point(field_get:stradsds.dshardctxmsg.alias)
  return *alias_;
}
inline void dshardctxmsg::set_alias(const ::std::string& value) {
  set_has_alias();
  if (alias_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    alias_ = new ::std::string;
  }
  alias_->assign(value);
  // @@protoc_insertion_point(field_set:stradsds.dshardctxmsg.alias)
}
inline void dshardctxmsg::set_alias(const char* value) {
  set_has_alias();
  if (alias_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    alias_ = new ::std::string;
  }
  alias_->assign(value);
  // @@protoc_insertion_point(field_set_char:stradsds.dshardctxmsg.alias)
}
inline void dshardctxmsg::set_alias(const char* value, size_t size) {
  set_has_alias();
  if (alias_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    alias_ = new ::std::string;
  }
  alias_->assign(reinterpret_cast<const char*>(value), size);
  // @@protoc_insertion_point(field_set_pointer:stradsds.dshardctxmsg.alias)
}
inline ::std::string* dshardctxmsg::mutable_alias() {
  set_has_alias();
  if (alias_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    alias_ = new ::std::string;
  }
  // @@protoc_insertion_point(field_mutable:stradsds.dshardctxmsg.alias)
  return alias_;
}
inline ::std::string* dshardctxmsg::release_alias() {
  clear_has_alias();
  if (alias_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    return NULL;
  } else {
    ::std::string* temp = alias_;
    alias_ = const_cast< ::std::string*>(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
    return temp;
  }
}
inline void dshardctxmsg::set_allocated_alias(::std::string* alias) {
  if (alias_ != &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    delete alias_;
  }
  if (alias) {
    set_has_alias();
    alias_ = alias;
  } else {
    clear_has_alias();
    alias_ = const_cast< ::std::string*>(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
  }
  // @@protoc_insertion_point(field_set_allocated:stradsds.dshardctxmsg.alias)
}

// required .stradsds.matrix_type mtype = 3;
inline bool dshardctxmsg::has_mtype() const {
  return (_has_bits_[0] & 0x00000004u) != 0;
}
inline void dshardctxmsg::set_has_mtype() {
  _has_bits_[0] |= 0x00000004u;
}
inline void dshardctxmsg::clear_has_mtype() {
  _has_bits_[0] &= ~0x00000004u;
}
inline void dshardctxmsg::clear_mtype() {
  mtype_ = 0;
  clear_has_mtype();
}
inline ::stradsds::matrix_type dshardctxmsg::mtype() const {
  // @@protoc_insertion_point(field_get:stradsds.dshardctxmsg.mtype)
  return static_cast< ::stradsds::matrix_type >(mtype_);
}
inline void dshardctxmsg::set_mtype(::stradsds::matrix_type value) {
  assert(::stradsds::matrix_type_IsValid(value));
  set_has_mtype();
  mtype_ = value;
  // @@protoc_insertion_point(field_set:stradsds.dshardctxmsg.mtype)
}

// required uint64 m_maxrow = 4;
inline bool dshardctxmsg::has_m_maxrow() const {
  return (_has_bits_[0] & 0x00000008u) != 0;
}
inline void dshardctxmsg::set_has_m_maxrow() {
  _has_bits_[0] |= 0x00000008u;
}
inline void dshardctxmsg::clear_has_m_maxrow() {
  _has_bits_[0] &= ~0x00000008u;
}
inline void dshardctxmsg::clear_m_maxrow() {
  m_maxrow_ = GOOGLE_ULONGLONG(0);
  clear_has_m_maxrow();
}
inline ::google::protobuf::uint64 dshardctxmsg::m_maxrow() const {
  // @@protoc_insertion_point(field_get:stradsds.dshardctxmsg.m_maxrow)
  return m_maxrow_;
}
inline void dshardctxmsg::set_m_maxrow(::google::protobuf::uint64 value) {
  set_has_m_maxrow();
  m_maxrow_ = value;
  // @@protoc_insertion_point(field_set:stradsds.dshardctxmsg.m_maxrow)
}

// required uint64 m_maxcol = 5;
inline bool dshardctxmsg::has_m_maxcol() const {
  return (_has_bits_[0] & 0x00000010u) != 0;
}
inline void dshardctxmsg::set_has_m_maxcol() {
  _has_bits_[0] |= 0x00000010u;
}
inline void dshardctxmsg::clear_has_m_maxcol() {
  _has_bits_[0] &= ~0x00000010u;
}
inline void dshardctxmsg::clear_m_maxcol() {
  m_maxcol_ = GOOGLE_ULONGLONG(0);
  clear_has_m_maxcol();
}
inline ::google::protobuf::uint64 dshardctxmsg::m_maxcol() const {
  // @@protoc_insertion_point(field_get:stradsds.dshardctxmsg.m_maxcol)
  return m_maxcol_;
}
inline void dshardctxmsg::set_m_maxcol(::google::protobuf::uint64 value) {
  set_has_m_maxcol();
  m_maxcol_ = value;
  // @@protoc_insertion_point(field_set:stradsds.dshardctxmsg.m_maxcol)
}


// @@protoc_insertion_point(namespace_scope)

}  // namespace stradsds

#ifndef SWIG
namespace google {
namespace protobuf {

template <> struct is_proto_enum< ::stradsds::matrix_type> : ::google::protobuf::internal::true_type {};
template <>
inline const EnumDescriptor* GetEnumDescriptor< ::stradsds::matrix_type>() {
  return ::stradsds::matrix_type_descriptor();
}

}  // namespace google
}  // namespace protobuf
#endif  // SWIG

// @@protoc_insertion_point(global_scope)

#endif  // PROTOBUF_ds_2eproto__INCLUDED
