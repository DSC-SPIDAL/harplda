/*
 *  Compress.h -- 简单封装一下zlibc库中常用的函数.
 * 
 *  Created: Zhang Minghui, Netera Inc.
 *
 *  Created: Dec. 9 9:34am 2005. version 0.1.1
 *              # A framework was given.
 */


#ifndef COMPRESS_H_ZMH_2005_12_09
#define COMPRESS_H_ZMH_2005_12_09

#include <iostream>
#include <string>
#include "zlib.h"

using namespace std;

class CompressException : public std::exception
{
public :
	//! Constructor.
	explicit
	CompressException(const string &msg) throw(): mMsg(msg){}
	
	//! Destructor.
	virtual ~CompressException() throw() {}

	//! 获取异常消息.
	virtual const char *what() const throw() {return mMsg.c_str();}

private :
	string mMsg;
};

class Compress
{
public :
	//! Constructor.
	Compress();

	//! Destructor.
	virtual ~Compress();

	/**
	 * @brief    将压缩过的串解压出来,由于原有的zlib.h中的uncompress里面参数的长度
	 *           和动态内存的申请过程比较烦琐，所以我用string来代替它.
	 *
	 * @param    result           存放解压结果.
	 * @param    rawLen           原始串的长度，告诉这个长度以便预申请空间.
	 * @param    compressedBytes  压缩过的串.
	 * @param    compressedLen    压缩串的长度.
	 * @return   压缩的结果标识.
	 * @retval   Z_OK             解压成功.
	 *
	 * 以下几种在uncompress原函数的返回值在此不会被返回，替换成抛出异常.
	 * @retval   Z_MEM_ERROR      没有足够的内存.
	 * @retval   Z_BUF_ERROR      输出缓存不够，这是zlib.h中的描述,在这里不会发生.
	 * @retval   Z_DATA_ERROR     输入数据不完整.
	 *
	 * @exception                 没有返回Z_OK便抛出异常，所以用户不要再通过函数
	 *                            返回值来判断解压情况了，应该捕捉异常.
	*/ 
	static int unCompress(string &result, int rawLen, 
			const char *compressedBytes, int compressedLen)
		throw(CompressException);

	//! unCompress的逆过程.
	static int compress(string &result, const char *source, int sourceLen)
		throw(CompressException);
protected :

private :

	//! bigpc上的zlib版本没有这个函数，我就给他加一个，我没有找到
	//        //! 这个函数的源代码，我通过他的规律判断他是这么做的.
	//                //! 后来找到了源码,就替换了自己发现的规律
	static uLong compressBound(uLong sourceLen) {
		return sourceLen + (sourceLen >> 12) + (sourceLen >> 14) + 11;
	}

};
#endif //COMPRESS_H_ZMH_2005_12_09
