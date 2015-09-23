/*
 *  TWReader.h -- 这个工具主要用来读取天网格式的存储文件.
 *
 *  Created: Zhang Minghui, Netera Inc.
 *
 *  Created: Nov. 26 11:06am 2005. version 0.1.1
 *              # A framework was given.
 */ 

#ifndef TWREADER_H_ZMH_2005_11_26
#define TWREADER_H_ZMH_2005_11_26

#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <sys/errno.h>
#include <unistd.h>
#include <string.h>


using namespace std;

class TWReaderException : public std::exception
{
public :
	//! Constructor.
	TWReaderException() throw() {}

	//! Construcor.
	TWReaderException(const string &msg) throw() : mMsg(msg){}

	//! 覆盖.
	const char *what() const throw() {return mMsg.c_str();}

	~TWReaderException() throw() {}

private :
	string mMsg;	//!< 异常消息内容.
};

class TWReader
{
public :
	//! 定义一个天网存储文件的记录类型. 天网文件格式请查看相关文档.
	typedef struct 
	{
		string version;		//!< 天网网页文件中每个记录的版本号.
		string id;		//!< ........................URL.
		string url;		//!< ........................URL.
		string date;		//!< ........................抓取日期.(待定)
		string ip;		//!< ........................ip地址.
		int    unzip_length;	//!< .................网页内容原始长度.
		int    length;		//!< .....................网页内容压缩长度.
		string body;		//!< ........................网页内容.
		void clear() {
			version.clear();
            id.clear();
			url.clear();
			date.clear();
			ip.clear();
			unzip_length = 0;
			length = 0;
			body.clear();
		}	//!< 将所有成员清空.
	} T_PageRecord;
	
public :
	//! Constructor without parameter.
	TWReader();
	
	//! Constructor.
	//! @param   twPageFile   天网网页文件.
	TWReader(const string &twPageFile) throw (TWReaderException);

	//! Destructor.
	virtual ~TWReader();

	/**
	 * @brief    接受新的天网网页文件.
	 *
	 * @param    twPageFile     文件名字.
	 */
	void input(const string &twPageFile) throw (TWReaderException);

	//! 返回天网文件中的下一个网页记录.
	//! @return   返回一个内容的指针.
	//! @retval   NULL : 表示文件结束.
	//! @retval   else : 返回正确结果.
	const T_PageRecord *nextRecord() throw (TWReaderException);

protected :

private :
	
private :
	T_PageRecord	mPageRecord;	//!< 为避免重复的构造该结构，将它做成该类的成员.
	ifstream	mTWFileStream;	//!< 天网网页文件流.
};
#endif //TWREADER_H_ZMH_2005_11_26
