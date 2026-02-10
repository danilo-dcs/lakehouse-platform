import { createTransport } from 'nodemailer'
import type { Transporter } from 'nodemailer'

import type { IMailingClient } from './IMailingClient'

type Service = 'gmail' | 'hotmail'

// import 'dotenv/config'

class MailingClient implements IMailingClient {
  private sender_email: string
  private sender_password: string
  private service: Service
  private subject?: string | undefined
  private text_body?: string | undefined
  private html_body?: string | undefined

  private transporter: Transporter

  constructor() {
    this.sender_email = String(process.env.EMAIL_USER)
    this.sender_password = String(process.env.EMAIL_PASS)
    this.service = String(process.env.EMAIL_SERVICE) as Service

    this.transporter = createTransport({
      service: this.service,
      auth: {
        user: this.sender_email,
        pass: this.sender_password,
      },
    })
  }

  public addSubject(subject: string): IMailingClient {
    this.subject = subject
    return this
  }

  public addTextBody(text: string): IMailingClient {
    this.text_body = text
    return this
  }

  public addHtmlBody(html: string): IMailingClient {
    this.html_body = html
    return this
  }

  public async sendEmail(reciever_address: string): Promise<boolean> {
    const mailOptions = {
      from: this.sender_email,
      to: reciever_address,
      subject: this.subject ?? 'New Access Request to Colletion on Data Lakehouse',
      text: this.text_body ?? '',
      html: this.html_body ?? '<p></p>',
    }

    const info = await this.transporter.sendMail(mailOptions)

    if (info) {
      return true
    }

    return false
  }
}

export default MailingClient
