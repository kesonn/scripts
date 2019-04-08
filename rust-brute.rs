extern crate mysql;
extern crate postgres;
extern crate ssh2;
extern crate redis;
extern crate telnet;
extern crate mongodb;
extern crate ftp;

use mysql::Pool;
use postgres::Connection;
use postgres::TlsMode;
use ssh2::Session;
use ftp::FtpStream;
use redis::Commands;
use telnet::{Telnet, TelnetEvent};
use mongodb::Client;


pub fn brute(){

}


/*

fn mysql(){}
fn mssql(){}
fn postgresql(){}
fn redis(){}
fn rsync(){}


extern crate mysql;
use mysql::Pool as mysqlpoll;
mysqlpoll:new("mysql://root:root@127.0.0.1:3306")

extern crate postgres;
use postgres::Connection as preconn;
use postgres::TlsMode;
preconn::connect("postgres://postgres@localhost:5433", TlsMode::None)

extern crate oracle;
use oracle::Connection as oraconn;
oraconn::connect("user", "pwd", "//localhost/XE", &[])?;


use ssh2::Session;
let tcp = TcpStream::connect("127.0.0.1:22").unwrap();
let mut sess = Session::new().unwrap();
sess.handshake(&tcp).unwrap();
sess.userauth_password("username", "password").unwrap();
assert!(sess.authenticated());


use ftp::FtpStream;
use ftp::openssl::ssl::{ SslContext, SslMethod };
let ftp_stream = FtpStream::connect("127.0.0.1:21").unwrap();
let ctx = SslContext::builder(SslMethod::tls()).unwrap().build();
let mut ftp_stream = ftp_stream.into_secure(ctx).unwrap();
ftp_stream.login("anonymous", "anonymous").unwrap();

extern crate redis;
use redis::Commands;
let client = redis::Client::open("redis://u:pwd@127.0.0.1/db")?;
let con = client.get_connection()?;

extern crate telnet;
use telnet::{Telnet, TelnetEvent};
let mut telnet = Telnet::connect(("ptt.cc", 23), 256);

extern crate mongodb;
use mongodb::Client;
let client = Client::connect_with_options("localhost", 27017, user, pwd)

let mut client = memcache::Client::connect("memcache://127.0.0.1:12345?timeout=10&tcp_nodelay=true").unwrap();


*/
fn main(){
    print!("dsds");
}