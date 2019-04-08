#!/usr/bin/env ruby
=begin
脚本功能为自动读取工资邮件并下载其附件
NOTE: 默认读取29天内，可以自行调整，配置选项 days: 29

首次使用，需要先通过以下命令，导出证书和私钥文件
 $ openssl pkcs12 -in <you.p12> -clcerts -nokeys -out crt.pem
 $ openssl pkcs12 -in <you.p12> -nocerts -out key.pem  # 会提示输入私钥密码，解密邮件时候需要
再将证书路径填入cert_path，私钥路径填入key_path
再配置邮箱账号和密码

加密的xls，也会自动调用msoffcrypto-tool工具进行解密后保存
msoffcrypto-tool的安装 pip install msoffcrypto-tool
=end
$opts = {
         email: 'xx_xxxxxxx@topsec.com.cn',
      password: 'xxxxxxxxxxxxxxxxxx',
     cert_path: 'crt.pem',
      key_path: 'key.pem',
          days: 29,
  xls_password: 'xxxxdddd' # 未安装msoffcrypto-tool 则可以不用填
}

# 
# 脚本主体
#
require 'openssl'
require 'mail'
require 'open3'

def puts_body(mail)
  puts
  puts "+------------------- 邮件内容 --------------------+"
  if body = mail.to_s[/<BODY>(.*?)<\/BODY>/m]
    puts body.gsub(/=\h\h/){|m| m[1,2].to_i(16).chr }.
          gsub(/=\n|<.*?>/, '').
          gsub("\r\n\r\n", "\n").
          encode 'utf-8', 'gb2312'
  end
end

def save_attachment(f)
  name = f.filename  
  n = 0
  name = "#{n+=1}-#{f.filename}" while File.exist? name
  puts "[+] 附件 \"#{name}\" 已保存"
  File.binwrite name, f.decoded
  de_name = name
  de_name = "#{n+=1}-#{f.filename}" while File.exist? de_name
  cmd = "msoffcrypto-tool -p '#{$opts[:xls_password]}' #{name} #{de_name}"
  out = Open3.popen2e(cmd){|_,out,_| out.read}
  puts "[+] 附件解密后保存在: \"#{de_name}\"" if out.empty?
end


if __FILE__ == $PROGRAM_NAME
  abort "[-] 证书文件不存在: \"#{$opts[:cert_path]}\"" unless File.exist? $opts[:cert_path]
  abort "[-] 私钥文件不存在: \"#{$opts[:key_path]}\"" unless File.exist? $opts[:key_path]

  Mail.defaults do retriever_method :imap, {
      :address    => "mail.topsec.com.cn",
      :port       => 993,
      :user_name  => $opts[:email],
      :password   => $opts[:password],
      :enable_ssl => true
    }
  end

  find_key = [
    'From',  "zhang_qiufang@topsec.com.cn",
    'Since', (DateTime.now - $opts[:days]).strftime('%d-%b-%Y')
  ]

  cert = OpenSSL::X509::Certificate.new(File::read($opts[:cert_path]))
  puts "[+] 输入私钥密码"
  while true
    begin
      key = OpenSSL::PKey::RSA.new(File::read($opts[:key_path]))
      break
    rescue OpenSSL::PKey::RSAError
      puts "[*] 密码错误，请重新输入"
    end
  end
  begin 
    Mail.find(keys: find_key) do |s_mail|
      p7enc = OpenSSL::PKCS7::read_smime(s_mail.to_s)

      data = p7enc.decrypt(key, cert)
      mime = Mail.read_from_string(data)
      mime = mime.decode_body[/Content-Type.*/m]
      mail = Mail.read_from_string(mime)
      puts_body(mail)
      mail.attachments.each do |file|
        save_attachment(file)
      end
    end
  rescue Net::OpenTimeout, Errno::ECONNRESET
    puts '[-] 公司邮箱好像出问题了'
  end
end
