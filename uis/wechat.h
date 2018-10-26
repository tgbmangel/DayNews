#ifndef WECHAT_H
#define WECHAT_H

#include <QDialog>

namespace Ui {
class WeChat;
}

class WeChat : public QDialog
{
    Q_OBJECT

public:
    explicit WeChat(QWidget *parent = nullptr);
    ~WeChat();

private:
    Ui::WeChat *ui;
};

#endif // WECHAT_H
