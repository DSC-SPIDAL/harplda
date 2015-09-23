/*
 * =====================================================================================
 * 
 *        Filename:  Compress.cpp
 * 
 *     Description:  
 * 
 *         Version:  1.0
 *         Created:  2005年12月14日 16时01分43秒 CST
 *        Revision:  none
 *        Compiler:  g++
 * 
 *          Author:  张明辉 (), zmh@netera.cn
 *         Company:  天网互联软件研发部
 * 
 * =====================================================================================
 */

#include "Compress.h"


int Compress::compress(string &result, const char *source, int sourceLen)
	throw (CompressException)
{
	uLong resultBoundLen = compressBound((uLong)sourceLen);

	result.resize((size_t)resultBoundLen);

	uLong realLen = resultBoundLen;
	int ret = ::compress((Bytef *)&result[0], (uLongf *)&realLen,
			(const Bytef *)source, (uLong)sourceLen);

	string msg = "Compress::compress() : ";
	switch (ret)
	{
	case Z_OK :
		result.resize(realLen);
		return Z_OK;
		break;
	case Z_MEM_ERROR :
		msg += "Z_MEM_ERROR 没有足够的内存.";
		throw CompressException(msg);
		break;
	case Z_BUF_ERROR :
		msg += "Z_BUF_ERROR 没有输出缓存.";
		throw CompressException(msg);
		break;
	default :
		break;
	}

	return Z_OK;
}

int Compress::unCompress(string &result, int rawLen, const char *compressedBytes, int compressedLen)
	throw (CompressException)
{
	//! rawLen主要是通过压缩时候存储留下的.
	//! 这个长度应该大于等于原串的长度，否则会出现缓冲区不足的错误.
	result.resize(rawLen);

	uLong realLen = (uLong)rawLen;
	int ret = ::uncompress((Bytef *)&result[0], (uLong *)&realLen,
			(Bytef *)compressedBytes, (uLong)compressedLen);

	string msg = "Compress::unCompress() : ";
	switch (ret)
	{
	case Z_OK :
		result.resize(realLen);
		return Z_OK;
	case Z_MEM_ERROR :
		msg += "Z_MEM_ERROR 没有足够的内存.";
		throw CompressException(msg);
		break;
	case Z_BUF_ERROR :
		msg += "Z_BUF_ERROR 没有输出缓存.";
		throw CompressException(msg);
		break;
	case Z_DATA_ERROR :
		msg += "Z_DATA_ERROR 输入数据有错.";
		throw CompressException(msg);
		break;
	default :
		break;
	}

	return Z_OK;
}


#ifdef _TEST


static void dohelp(int argc, char *argv[])
{
	cout << "usage : " << argv[0] << " string" << endl;
	return;
}

int main(int argc, char *argv[])
{
	if (argc != 2)
	{
		dohelp(argc, argv);
		return 1;
	}

	string compressed;

	try {
		Compress::compress(compressed, argv[1], strlen(argv[1]));

		cout << "the raw len : " << strlen(argv[1]) << endl;
		cout << "after compressing len : " << compressed.length() << endl;

		string uncompressed;

		Compress::unCompress(uncompressed, strlen(argv[1]),
				compressed.c_str(), compressed.length());

		cout << "after uncompressing : " << uncompressed << endl;
	} catch (CompressException &E) {
		cout << E.what() << endl;
	} catch (exception &E) {
		cout << E.what() << endl;
	}

	return 0;
}
#endif //_TEST
