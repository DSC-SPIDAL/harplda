/*
 *  Compress.h -- �򵥷�װһ��zlibc���г��õĺ���.
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

	//! ��ȡ�쳣��Ϣ.
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
	 * @brief    ��ѹ�����Ĵ���ѹ����,����ԭ�е�zlib.h�е�uncompress��������ĳ���
	 *           �Ͷ�̬�ڴ��������̱ȽϷ�������������string��������.
	 *
	 * @param    result           ��Ž�ѹ���.
	 * @param    rawLen           ԭʼ���ĳ��ȣ�������������Ա�Ԥ����ռ�.
	 * @param    compressedBytes  ѹ�����Ĵ�.
	 * @param    compressedLen    ѹ�����ĳ���.
	 * @return   ѹ���Ľ����ʶ.
	 * @retval   Z_OK             ��ѹ�ɹ�.
	 *
	 * ���¼�����uncompressԭ�����ķ���ֵ�ڴ˲��ᱻ���أ��滻���׳��쳣.
	 * @retval   Z_MEM_ERROR      û���㹻���ڴ�.
	 * @retval   Z_BUF_ERROR      ������治��������zlib.h�е�����,�����ﲻ�ᷢ��.
	 * @retval   Z_DATA_ERROR     �������ݲ�����.
	 *
	 * @exception                 û�з���Z_OK���׳��쳣�������û���Ҫ��ͨ������
	 *                            ����ֵ���жϽ�ѹ����ˣ�Ӧ�ò�׽�쳣.
	*/ 
	static int unCompress(string &result, int rawLen, 
			const char *compressedBytes, int compressedLen)
		throw(CompressException);

	//! unCompress�������.
	static int compress(string &result, const char *source, int sourceLen)
		throw(CompressException);
protected :

private :

	//! bigpc�ϵ�zlib�汾û������������Ҿ͸�����һ������û���ҵ�
	//        //! ���������Դ���룬��ͨ�����Ĺ����ж�������ô����.
	//                //! �����ҵ���Դ��,���滻���Լ����ֵĹ���
	static uLong compressBound(uLong sourceLen) {
		return sourceLen + (sourceLen >> 12) + (sourceLen >> 14) + 11;
	}

};
#endif //COMPRESS_H_ZMH_2005_12_09
